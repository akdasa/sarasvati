from api.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__database = None
        self.__application = SarasvatiConsoleApplication()

    def activate(self):
        print("Sarasvati Console Interface")
        self.__database = self.api.plugins.get("database")
        print("  database:", self.__database.name, self.__database.version)
