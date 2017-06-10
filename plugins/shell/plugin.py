from logging import info

from sarasvati.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__application = None

    def activate(self):
        self.__application = SarasvatiConsoleApplication()
        self.__application.run()
