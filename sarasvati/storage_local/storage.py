import random


from api.models import Thought, IdentityComponent, DefinitionComponent, LinksComponent
from .internal import InternalStorage
from .cache import StorageCache


class LocalStorage:
    def __init__(self, path="db.json"):
        """Initializes new instance of the LocalStorage class."""
        super().__init__()
        self.__cache = StorageCache()
        self.__db = InternalStorage(path)

        # serialization options
        self._options = {
            IdentityComponent.COMPONENT_NAME: IdentityComponent,
            DefinitionComponent.COMPONENT_NAME: DefinitionComponent,
            LinksComponent.COMPONENT_NAME: LinksComponent}

    @property
    def cache(self):
        return self.__cache

    def count(self):
        return self.__db.count()

    def contains(self, key):
        return self.__db.contains(key)

    def get(self, key, options=None):
        """
        Returns thought by "identity.key"
        :param key: Key
        :param options: Options
        :return: Thought or None if nothing found
        """
        if self.__cache.is_cached_with_links(key):
            return self.__cache.get(key)
        result = self.search({
            "field": "identity.key",
            "operator": "=",
            "value": key}, options)
        if len(result) > 1:
            raise Exception("Entity is not unique {}".format(key))
        return result[0] if len(result) > 0 else None

    def add(self, thought):
        """
        Adds thought to storage
        :type thought: Thought
        :param thought: Thought
        """
        if self.contains(thought.key):
            raise Exception("Thought this same key '{}/{}' already exist".format(thought.key, thought.title))
        data = thought.serialization.serialize()
        self.__db.insert(data)
        self.__cache.add(thought)

    def update(self, thought):
        """
        Updates thought
        :type thought: Thought
        :param thought: Thought to update 
        """
        data = thought.serialization.serialize()
        self.__db.update(thought.key, data)

    def remove(self, thought):
        """
        Removes thought from storage
        :type thought: Thought
        :param thought: Thought
        """
        self.__db.remove(thought.key)
        self.__cache.remove(thought)

    def search(self, query, options=None):
        x = random.randint(0, 100)
        print(x, "---  ---  ---")
        print("QUERY", query)
        if options is None:
            options = {}
        options.update(self._options)
        options["storage"] = self
        if "depth" not in options:
            options["depth"] = 0

        result = []
        db_search_result = self.__db.search(query)
        for db_entity in db_search_result:
            key = db_entity["identity"]["key"]
            in_cache = key in self.cache.thoughts
            is_lazy = self.__cache.is_lazy(key)

            print("DB_RESULT", in_cache, is_lazy)

            if in_cache:
                # get thought from cache
                cached = self.__cache.thoughts[key]

                # thought is in lazy state, so load it
                if is_lazy:
                    #self.cache.lazy[cached.key] = False
                    print("DESERIALIZE", db_entity)
                    self.__cache.add(cached, lazy=False)
                    cached.serialization.deserialize(db_entity, options)

                # thought have lazy links
                for linked_thought in cached.links.all:
                    if not self.__cache.is_lazy(linked_thought.key):
                        continue  # skip not lazy thought
                    #self.cache.lazy[linked_thought.key] = False
                    #db_lazy_linked = self.__db.search(Query().identity.key == linked_thought.key)[0]
                    db_lazy_linked = self.__db.search({
                        "field": "identity.key",
                        "operator": "=",
                        "value": linked_thought.key})[0]
                    print("DESERIALIZE LAZY CHILD", db_lazy_linked)
                    self.cache.add(linked_thought)
                    linked_thought.serialization.deserialize(db_lazy_linked, options)
                result.append(self.__cache.thoughts[key])
            else:
                # use "depth" options to avoid all DB deserialization
                # by going links deeper and deeper
                not_deep = options["depth"] < 2

                # create new thought
                new_thought = Thought()

                # pre-cache to avoid infinitive recursion
                if query["field"] == "identity.key":
                    new_thought.identity.key = query["value"]
                    self.cache.add(new_thought, key=query["value"])

                if not_deep:
                    # deserialize and add to result
                    print("DESERIALIZE", db_entity)
                    new_thought.serialization.deserialize(db_entity, options)
                    self.__cache.add(new_thought)
                    result.append(new_thought)
                else:
                    print("TOO DEEP", query["value"])
                    new_thought.identity.key = query["value"]
                    self.cache.add(new_thought, lazy=True)
                    result.append(new_thought)

        print(x, result)
        return result

