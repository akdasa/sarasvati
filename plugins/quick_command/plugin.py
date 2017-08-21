from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent

from sarasvati.plugins import ToolboxPlugin
from .toolbox import QuickCommandToolbox


class QuickCommandToolboxPlugin(ToolboxPlugin):
    def activate(self):
        pass

    def get(self, engine):
        qmlRegisterType(QuickCommandToolbox, 'QuickCommandToolbox', 1, 0, 'QuickCommandToolbox')
        path = "plugins/quick_command/QuickCommandToolbox.qml"  # todo

        component = QQmlComponent(engine)
        component.loadUrl(QUrl(path))
        item = component.create()
        return item
