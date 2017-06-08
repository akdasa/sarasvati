from logging import info

from sarasvati.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    __BYE_MESSAGE = "Good bye, take care!"

    def __init__(self):
        super().__init__()
        self.__application = None
        self.__storage = None
        self.__commands = None

    def activate(self):
        # load required plugins
        self.__storage = self._api.plugins.get("storage")
        self.__commands = self._api.plugins.find("commands")
        info("storage: {} {}".format(self.__storage.info.name, self.__storage.info.version))
        info("commands: {} plugin(s) loaded".format(len(self.__commands)))

        # create and run application
        self.__application = SarasvatiConsoleApplication(
            storage_plugin=self.__storage, command_plugins=self.__commands)
        self.__application.run()

    def deactivate(self):
        print(self.__BYE_MESSAGE)
