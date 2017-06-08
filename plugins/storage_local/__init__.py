from sarasvati.plugins import StoragePlugin
from .storage import LocalStorage


class LocalStoragePlugin(StoragePlugin):
    def __init__(self):
        """Initializes new instance of the LocalStoragePlugin class."""
        super().__init__()
        self.__storage = LocalStorage()

    def get_storage(self):
        return self.__storage
