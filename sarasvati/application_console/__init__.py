from api.instance import get_api
from api.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    __INDENT = ".."
    __BYE_MESSAGE = "Good bye, take care!"

    def __init__(self):
        super().__init__()
        self.__application = None
        self.__storage = None
        self.__commands = None
        self.__api = get_api()

    def activate(self):
        # Load required plugins
        self.__storage = self.__api.plugins.get("storage")
        self.__commands = self.__api.plugins.find("commands")
        print(self.__INDENT, "storage:", self.__storage.info.name, self.__storage.info.version)
        print(self.__INDENT, "commands:", len(self.__commands), "plugin(s) loaded")

        # Create and run application
        self.__application = SarasvatiConsoleApplication(
            storage_plugin=self.__storage, command_plugins=self.__commands)
        self.__application.run()

    def deactivate(self):
        print(self.__BYE_MESSAGE)
