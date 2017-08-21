from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickItem

from sarasvati import get_api


class QuickEditToolbox(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thought = None
        get_api().events.thought_activated.subscribe(self.__thought_activated)

    activated = pyqtSignal(str, str, arguments=['thought_title', 'thought_description'])

    @pyqtSlot(str, str, name="changed")
    def changed(self, title, description):
        if not self.__thought:
            return
        self.__thought.title = title
        self.__thought.description = description
        get_api().brain.storage.update(self.__thought)

    def __thought_activated(self, thought):
        self.__thought = thought
        self.activated.emit(thought.title,
                            thought.description or "")
