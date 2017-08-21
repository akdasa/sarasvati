from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickItem


class QuickEditToolbox(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)

    activated = pyqtSignal(dict, arguments=['data'])

    @pyqtSlot(str, name="execute")
    def execute(self, line):
        print("123" + line)
        self.activated.emit({"test": 123})
