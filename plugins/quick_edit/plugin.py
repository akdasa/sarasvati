import os

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent

from sarasvati.plugins import ToolboxPlugin
from .toolbox import QuickEditToolbox


class QuickEditToolboxPlugin(ToolboxPlugin):
    def __init__(self):
        super().__init__()
        self.__qml_path = None

    def activate(self):
        qmlRegisterType(QuickEditToolbox, 'QuickEditToolbox', 1, 0, 'QuickEditToolbox')
        self.__qml_path = os.path.join(self.info.path, "QuickEditToolbox.qml")

    def get(self, engine):
        component = QQmlComponent(engine)
        component.loadUrl(QUrl(self.__qml_path))
        item = component.create()
        return item
