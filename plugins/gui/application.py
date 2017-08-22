import sys

from PyQt5.QtCore import QMetaObject, Qt, Q_ARG, QVariant
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem

from sarasvati.application import SarasvatiApplication
from .controllers import *


class SarasvatiGuiApplication(SarasvatiApplication):
    def __init__(self):
        super().__init__()
        self.__app = None
        self.__plex = PlexController()
        self.__processor = ProcessorController()
        self.__brain = BrainController()
        self._api.events.message.subscribe(self.__on_message)

    # noinspection PyUnresolvedReferences
    def run(self):
        self.__app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("plex", self.__plex)
        engine.rootContext().setContextProperty("processor", self.__processor)
        engine.rootContext().setContextProperty("brain", self.__brain)

        engine.load("plugins/gui/ui/views/App.qml")  # todo
        engine.quit.connect(self.__app.quit)

        self.__init_panel(engine)

        sys.exit(self.__app.exec_())

    def __init_panel(self, engine):
        window = engine.rootObjects()[0]
        container = window.findChild(QQuickItem, "panel")

        toolboxes = self._api.plugins.find("toolbox")
        for toolbox in toolboxes:
            itm = toolbox.get(engine)
            QMetaObject.invokeMethod(container, "append", Qt.DirectConnection, Q_ARG(QVariant, itm))

    def __on_message(self, args):
        message, state = args
        self.__processor.commandResult.emit(message, state)
