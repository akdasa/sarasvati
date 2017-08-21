import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQuick import QQuickItem

from sarasvati import get_api


class QuickCommandToolbox(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__api = get_api()

    @pyqtSlot(str, name="execute")
    def execute(self, line):
        try:
            result = self.__api.execute(line)
            if hasattr(result, "message"):
                self.commandResult.emit(result.message, True)
        except Exception:
            logging.exception("Exception")
