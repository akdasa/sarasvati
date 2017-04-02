from api.plugins import ApplicationPlugin
from .application import SarasvatiConsoleApplication


class SarasvatiConsoleApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()
        self.__application = SarasvatiConsoleApplication()

    def activate(self):
        print("Activating console interface")
