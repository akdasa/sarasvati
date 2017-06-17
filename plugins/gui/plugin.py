from sarasvati.plugins import ApplicationPlugin
from .application import SarasvatiGuiApplication


class SarasvatiGuiApplicationPlugin(ApplicationPlugin):
    def __init__(self):
        super().__init__()

    def activate(self):
        SarasvatiGuiApplication().run()
