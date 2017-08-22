from sarasvati.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__app = None

    def activate(self):
        self.__app = SarasvatiConsoleApplication()
        self.__app.run()
