from sarasvati.plugins import StoragePlugin
from .storage import LocalStorage


class LocalStoragePlugin(StoragePlugin):
    def __init__(self):
        super().__init__()
        self.__serializer = None

    def open(self, path):
        return LocalStorage(path)
