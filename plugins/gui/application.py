import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from plugins.gui.controllers import *
from sarasvati.application import SarasvatiApplication


class SarasvatiGuiApplication(SarasvatiApplication):
    def __init__(self):
        super().__init__()
        self.__app = None
        self.__plex = PlexController()
        self.__processor = ProcessorController()

    def run(self):
        self.__app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("plex", self.__plex)
        engine.rootContext().setContextProperty("processor", self.__processor)
        engine.load("plugins/gui/ui/views/App.qml")  # todo
        engine.quit.connect(self.__app.quit)
        sys.exit(self.__app.exec_())
