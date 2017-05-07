from api.instance import get_api
from api.plugins import ApplicationPlugin
from .application import SarasvatiGuiApplication


class SarasvatiGuiApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__application = None
        self.__storage = None
        self.__commands = None
        self.__sections = None
        self.__api = get_api()

    def activate(self):
        # Load required plugins
        self.__storage = self.__api.plugins.get("storage")
        self.__commands = self.__api.plugins.find("commands")
        self.__sections = self.__api.plugins.find("section")

        # Create and run application
        self.__application = SarasvatiGuiApplication(
            storage_plugin=self.__storage, section_plugins=self.__sections)
        self.__application.run()
