from api.plugins import ApplicationPlugin
from .application import SarasvatiGuiApplication


class SarasvatiGuiApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__application = None
        self.__storage = None
        self.__commands = None
        self.__sections = None

    def activate(self):
        # Load required plugins
        self.__storage = self.api.plugins.get("storage")
        self.__commands = self.api.plugins.find("commands")
        self.__sections = self.api.plugins.find("section")

        # Create and run application
        self.__application = SarasvatiGuiApplication(
            storage_plugin=self.__storage, section_plugins=self.__sections)
        self.__application.run()
