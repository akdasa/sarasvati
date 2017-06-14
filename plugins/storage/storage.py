from sarasvati import get_api
from sarasvati.brain import Thought
from sarasvati.storage import Storage
from .cache import StorageCache
from .internal import InternalStorage


class LocalStorage(Storage):
    def __init__(self, path="db.json"):
        """
        Initializes new instance of the LocalStorage class
        :type path: str
        :param path: path
        """
        super().__init__()
        self.__cache = StorageCache()
        self.__db = InternalStorage(path)
        self.__options = get_api().serialization.get_options(self)

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
        # delete references to thought
        for linked in thought.links.all:
            linked.links.remove(thought)
            self.update(linked)

        # remove thought itself
        if self.__db.contains(thought.key):
            self.__db.remove(thought.key)
            self.__cache.remove(thought)
        else:
            raise Exception("Unable to remove a non-existent thought")

    def search(self, query):
        """
        Search
        :param query: Query 
        :return: Array of thoughts if found 
        """
        # try get query result from cache first
        result = self.__try_get_from_cache(query)

        # nothing found, fetch data from db
        if not result:  # get it from db
            db_search_result = self.__db.search(query)
            for db_entity in db_search_result:
                thought = self.__process_db_entry(db_entity)
                self.__cache.add(thought)
                result.append(thought)

        # load linked thoughts
        for thought in result:
            self.__load_linked(thought)

        return result

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

    def contains(self, key):
        """
        Returns True if storage contains thought with specified key
        :rtype: bool
        :type key: str
        :param key: Key
        :return: True if thought found in storage
        """
        return self.__db.contains(key)

    def count(self, query=None):
        """
        Returns count of Thoughts
        :type query: dict
        :rtype: int
        :param query: Query
        :return: Count
        """
        return self.__db.count(query)

    @property
    def cache(self):
        """
        Returns cache
        """
        return self.__cache

    def __process_db_entry(self, db_entity):
        try:
            key = db_entity["identity"]["key"]
            cached, lazy = self.__cache.status(key)
            thought = cached or Thought()
            if not cached or lazy:
                thought.serialization.deserialize(db_entity, self.__options)
            return thought
        except:
            raise Exception("Error while processing DB entry")

    def __try_get_from_cache(self, query):
        if query["field"] == "identity.key" and query["operator"] == "=":
            key = query["value"]
            cached, is_lazy = self.__cache.status(key)
            if cached and not is_lazy:
                return [cached]
        return []

    def __load_linked(self, thought):
        lazy_links = filter(lambda x: self.__cache.is_lazy(x.key), thought.links.all)
        for linked in lazy_links:
            db_data = self.__db.search({"field": "identity.key", "operator": "=", "value": linked.key})
            if len(db_data) == 0:
                raise Exception("No link '{}' found".format(linked.key))
            linked.serialization.deserialize(db_data[0], self.__options)
            self.__cache.add(linked, lazy=False)
