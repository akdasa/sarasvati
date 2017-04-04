from api.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    __INDENT = ".."

    def __init__(self):
        super().__init__()
        self.__application = None
        self.__database = None
        self.__commands = None

    def activate(self):
        # Load required plugins
        self.__database = self.api.plugins.get("database")
        self.__commands = self.api.plugins.find("commands")
        print(self.__INDENT, "database:", self.__database.name, self.__database.version)
        print(self.__INDENT, "commands:", len(self.__commands), "plugin(s) loaded")

        # Create and run application
        self.__application = SarasvatiConsoleApplication(
            database_plugin=self.__database, command_plugins=self.__commands)
        self.__application.run()

    def deactivate(self):
        print("Good bye!")
