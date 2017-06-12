from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
import logging


class InternalStorage:
    def __init__(self, path):
        self.__logger = logging.getLogger("storage")
        if path is not None:
            self.__db = TinyDB(path)
        else:
            self.__db = TinyDB(storage=MemoryStorage)

    def count(self, query=None):
        return len(self.__db)

    def contains(self, key):
        return self.__db.contains(Query().identity.key == key)

    def insert(self, data):
        self.__db.insert(data)

    def update(self, key, data):
        self.__logger.debug("Update '{}' with '{}'".format(key, data))
        self.__db.update(
            _update_operation(data),
            Query().identity.key == key)

    def remove(self, key):
        self.__logger.debug("Remove {}".format(key))
        return self.__db.remove(Query().identity.key == key)

    def search(self, query):
        self.__logger.debug("Search {}".format(query))
        db_query = self.__tiny_db_query(query)
        return self.__db.search(db_query)

    @staticmethod
    def __tiny_db_query(query):
        result = Query()
        field = query["field"]
        value = query["value"]
        for p in field.split("."):
            result = result[p]
        if query["operator"] in ["eq", "="]:
            result = result == value
        if query["operator"] in ["contains", "~"]:
            result = result.test(lambda x: value in x)
        if query["operator"] in ["contains_case_insensitive", "~~"]:
            result = result.test(lambda x: value.lower() in x.lower())
        return result


def _update_operation(data):
    def transform(element):
        element.update(data)
    return transform
