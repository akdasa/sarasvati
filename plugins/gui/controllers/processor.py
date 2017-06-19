from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from pycopa.exception import PycopaException

from sarasvati import get_api
from sarasvati.commands import CommandException


class ProcessorController(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__api = get_api()

    commandResult = pyqtSignal(str, bool, arguments=['message', 'successful'])

    @pyqtSlot(str, name="execute")
    def execute(self, line):
        try:
            result = self.__api.processor.execute(line)
            if hasattr(result, "message"):
                self.commandResult.emit(result.message, True)
        except CommandException as ex:
            # todo write log
            self.commandResult.emit(ex.args[0], False)
        except PycopaException as ex:
            self.commandResult.emit("Syntax error: {}".format(ex.args[0]), False)
        except Exception as ex:
            self.commandResult.emit(ex.args[0], False)
