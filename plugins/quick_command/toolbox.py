import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQuick import QQuickItem
from pycopa.exception import PycopaException

from sarasvati import get_api
from sarasvati.commands import CommandException


class QuickCommandToolbox(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__api = get_api()
        self.__send = self.__api.events.message

    @pyqtSlot(str, name="execute")
    def execute(self, line):
        try:
            result = self.__api.execute(line)
            if hasattr(result, "message"):
                self.__send.notify((result.message, True))
        except CommandException as ex:
            logging.exception("Command exception")
            self.__send.notify((ex.args[0], False))
        except PycopaException as ex:
            logging.exception("Syntax error")
            self.__send.notify(("Syntax error: {}".format(ex.args[0]), False))
        except Exception as ex:
            logging.exception("Exception")
            self.__send.notify((ex.args[0], False))
