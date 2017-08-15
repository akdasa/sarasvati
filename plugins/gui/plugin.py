from sarasvati.plugins import ApplicationPlugin
from .application import SarasvatiGuiApplication


class SarasvatiGuiApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__app = None

    def activate(self):
        self.__app = SarasvatiGuiApplication()
        self.__app.run()
