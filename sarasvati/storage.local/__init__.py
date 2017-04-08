from tinydb import TinyDB, Query

from api.models import Thought, IdentityComponent, DefinitionComponent, LinksComponent
from api.plugins import StoragePlugin


class LocalStoragePlugin(StoragePlugin):
    def __init__(self, path="db.json", storage=None):
        """Initializes new instance of the LocalStorage class."""
        super().__init__()
        #self.__serialization = Serialization()
        #self.__serialization.register(IdentityComponent)
        #self.__serialization.register(DefinitionComponent)
        #self.__serialization.register(LinksComponent)
        self._s = {IdentityComponent.COMPONENT_NAME: IdentityComponent, DefinitionComponent.COMPONENT_NAME: DefinitionComponent, LinksComponent.COMPONENT_NAME: LinksComponent}

        if not storage:
            self.__db = TinyDB(path)
        else:
            self.__db = TinyDB(storage=storage)
        self.__cache = {}  # TODO: extract to separate class
        self.__lazy = {}

    def count(self):
        return 0  # len(self.__storage)

    def get(self, key, options=None):
        """
        Returns thought by "identity.key"
        :param key: Key
        :param options: Options
        :return: Thought or None if nothing found
        """
        if key in self.__cache:
            return self.__cache[key]
        result = self.search({
            "field": "identity.key",
            "operator": "=",
            "value": key}, options)
        return result[0] if len(result) > 0 else None

    def add(self, thought):
        """
        Adds thought to storage
        :param thought: Thought
        """
        #data = self.__serialization.serialize(thought)
        data = thought.serialization.serialize()
        self.__db.insert(data)

    def update(self, thought):
        #data = self.__serialization.serialize(thought)
        data = thought.serialization.serialize()

        def your_operation():
            def transform(element):
                element.update(data)
            return transform

        self.__db.update(your_operation(), Query()["identity"]["key"] == thought.key)

    def remove(self, thought):
        """
        Removes thought from storage
        :param thought: Thought
        """
        query = Query()
        self.__db.remove(query.identity.key == thought.key)
        if thought.key in self.__cache:
            del self.__cache[thought.key]

    def search(self, query, options=None):
        q = Query()
        field = query["field"]
        value = query["value"]
        result = []

        options = (options or {"storage": self, "depth": 0}).copy()
        #storage = options["storage"]

        for p in field.split("."):
            q = q[p]

        if query["operator"] in ["eq", "="]:
            q = q == value

        if query["operator"] in ["contains", "~"]:
            q = q.test(lambda x: value in x)

        if query["operator"] in ["contains_case_insensitive", "~~"]:
            q = q.test(lambda x: value.lower() in x.lower())

        search_result = self.__db.search(q)
        for entity in search_result:
            key = entity["identity"]["key"]
            in_cache = key in self.__cache
            in_lazy = key in self.__lazy

            if in_cache:
                print("[FROM CACHE] " + key)
                cached = self.__cache[key]

                # thought in lazy state. Load data fron DB and deserialize it.
                if in_lazy:
                    #print("[LOAD LAZY] " + key)
                    lazy_result = self.__db.search(Query().identity.key == key)[0]
                    #cached.serialization.deserialize(lazy_result, options)
                    #self.__serialization.deserialize(cached, lazy_result, options)
                    cached.serialization.deserialize(lazy_result, {**options, **self._s})
                    del self.__lazy[key]

                # thought have lazy links. Load it.
                for thought in cached.links.all:
                    if thought.key not in self.__lazy:
                        continue  # skip not lazy thought
                    print("[LAZY CHILD] " + thought.key)
                    lazy_child = self.__db.search(Query().identity.key == thought.key)[0]
                    #thought.serialization.deserialize(lazy_child)
                    #self.__serialization.deserialize(thought, lazy_child)
                    thought.serialization.deserialize(lazy_child, self._s)
                    del self.__lazy[thought.key]

                result.append(cached)

            else:
                # use "depth" options to avoid all DB deserialization by going links deeper and deeper
                not_depth_specified = options is None or ("depth" not in options)
                not_deep = not_depth_specified or options["depth"] < 2

                t = Thought()
                if field == "identity.key":
                    print("[TO CACHE] " + key)
                    self.__cache[value] = t  # pre-cache to avoid infinitive recursion

                if not_deep:
                    print("[DESERIALIZE]: ", entity)
                    print("[TO CACHE] " + key)
                    self.__cache[key] = t
                    #self.__serialization.deserialize(t, entity, options)
                    t.serialization.deserialize(entity, {**options, **self._s})
                else:
                    # we are going to deep. Just stop here. Mark thought as
                    # lazy and load it when required.
                    print("[ADD LAZY] " + key)
                    self.__lazy[key] = t
                    t.identity.key = key
                    t.title = t.description = "<LAZY>"

                result.append(t)

        return result
