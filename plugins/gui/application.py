import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from sarasvati.application import SarasvatiApplication
from .controllers import *


class SarasvatiGuiApplication(SarasvatiApplication):
    def __init__(self):
        super().__init__()
        self.__app = None
        self.__plex = PlexController()
        self.__processor = ProcessorController()
        self.__brain = BrainController()

    def run(self):
        self.__app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("plex", self.__plex)
        engine.rootContext().setContextProperty("processor", self.__processor)
        engine.rootContext().setContextProperty("brain", self.__brain)
        engine.load("plugins/gui/ui/views/App.qml")  # todo
        engine.quit.connect(self.__app.quit)
        sys.exit(self.__app.exec_())
