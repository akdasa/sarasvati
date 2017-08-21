from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent

from plugins.quick_edit.toolbox import QuickEditToolbox
from sarasvati.plugins import ToolboxPlugin


class QuickEditToolboxPlugin(ToolboxPlugin):
    def activate(self):
        pass

    def get(self, engine):
        qmlRegisterType(QuickEditToolbox, 'QuickEditToolbox', 1, 0, 'QuickEditToolbox')
        path = "plugins/quick_edit/QuickEditToolbox.qml"  # todo

        component = QQmlComponent(engine)
        component.loadUrl(QUrl(path))
        item = component.create()
        return item
