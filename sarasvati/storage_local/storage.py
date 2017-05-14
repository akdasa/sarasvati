from api.brain import Thought
from api.brain.model import IdentityComponent
from api.brain.thought import DefinitionComponent, LinksComponent
from .cache import StorageCache
from .internal import InternalStorage


class LocalStorage:
    def __init__(self, path="db.json"):
        """
        Initializes new instance of the LocalStorage class
        :type path: str
        :param path: path
        """
        super().__init__()
        self.__cache = StorageCache()
        self.__db = InternalStorage(path)
        self._options = {
            "get_component": self.__get_component,
            "get_linked": self.get_from_cache_or_create}

    @property
    def cache(self):
        return self.__cache

    def count(self):
        return self.__db.count()

    def contains(self, key):
        return self.__db.contains(key)

    def get(self, key):
        """
        Returns thought by "identity.key"
        :param key: Key
        :return: Thought or None if nothing found
        """
        result = self.search({
            "field": "identity.key",
            "operator": "=",
            "value": key})
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
            raise Exception("Thought with same key '{}/{}' already exist".format(thought.key, thought.title))
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

    def search(self, query):
        """
        Search
        :param query: Query 
        :return: Array of thoughts if found 
        """
        result = []

        # if search for one thought
        if query["field"] == "identity.key" and query["operator"] == "=":
            if self.__cache.is_cached_with_links(query["value"]):
                return [self.__cache.get(query["value"])]
            elif self.__cache.is_cached(query["value"]) and not self.__cache.is_lazy(query["value"]):
                thought = self.__cache.get(query["value"])
                self.__load_linked(thought)
                return [thought]

        # get it from db
        db_search_result = self.__db.search(query)
        for db_entity in db_search_result:
            key = db_entity["identity"]["key"]
            in_cache = self.__cache.is_cached(key)
            is_lazy = self.__cache.is_lazy(key)

            if not in_cache:
                thought = Thought()
                thought.serialization.deserialize(db_entity, self._options)
                self.__cache.add(thought)
                self.__load_linked(thought)
            else:
                thought = self.__cache.get(key)
                if is_lazy:
                    thought.serialization.deserialize(db_entity, self._options)
                    self.__cache.add(thought)  # remove lazy flag
                self.__load_linked(thought)

            result.append(thought)

        return result

    def __load_linked(self, thought):
        for linked in thought.links.all:
            if self.__cache.is_lazy(linked.key):
                db_data = self.__db.search({"field": "identity.key", "operator": "=", "value": linked.key})
                if len(db_data) == 0:
                    raise Exception("No link '{}' found".format(linked.key))
                linked.serialization.deserialize(db_data[0], self._options)
                self.__cache.add(linked, lazy=False)

    @staticmethod
    # TODO: set serialization map
    def __get_component(key):
        options = {
            IdentityComponent.COMPONENT_NAME: IdentityComponent,
            DefinitionComponent.COMPONENT_NAME: DefinitionComponent,
            LinksComponent.COMPONENT_NAME: LinksComponent}
        res = options.get(key, None)
        if res:
            return res()
        return None

    def get_from_cache_or_create(self, key):
        cached = self.__cache.thoughts.get(key, None)
        if not cached:
            thought = Thought("<LAZY>", key=key)
            self.__cache.add(thought, lazy=True)
            return thought
        else:
            return cached
