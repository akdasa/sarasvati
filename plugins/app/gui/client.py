import logging
import sys

from PyQt5.QtCore import QMetaObject, Qt, Q_ARG, QVariant
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem


class Client:
    def __init__(self, api, controllers):
        self.__app = None
        self.__api = api
        self.__plex = controllers.get("plex")
        self.__processor = controllers.get("processor")
        self.__brain = controllers.get("brain")

    def run(self):
        self.__app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("plex", self.__plex)
        engine.rootContext().setContextProperty("processor", self.__processor)
        engine.rootContext().setContextProperty("brain", self.__brain)

        engine.load("plugins/app/gui/ui/views/App.qml")  # todo
        engine.quit.connect(self.__app.quit)

        self.__api.events.message.subscribe(self.__on_message)
        self.__init_panel(engine)
        self.__create_root_thought()

        sys.exit(self.__app.exec_())

    def __create_root_thought(self):
        # Create root thought
        if not self.__api.storage.contains("Root"):
            self.__api.execute("/c Root key:Root")
        self.__api.execute("/a key:Root")

    def __init_panel(self, engine):
        window = engine.rootObjects()[0]
        container = window.findChild(QQuickItem, "panel")

        toolboxes = self.__api.plugins.find("toolbox")
        for toolbox in toolboxes:
            try:
                toolbox.activate()
                itm = toolbox.get(engine)
                QMetaObject.invokeMethod(container, "append", Qt.DirectConnection, Q_ARG(QVariant, itm))
            except Exception:
                logging.error("Unable to instantiate {} toolbox".format(toolbox.__class__.__name__))
                pass

    def __on_message(self, args):
        message, state = args
        self.__processor.commandResult.emit(message, state)
