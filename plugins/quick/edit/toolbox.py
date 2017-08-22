from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickItem

from sarasvati import get_api


class QuickEditToolbox(QQuickItem):
    activated = pyqtSignal(str, str, arguments=['thought_title', 'thought_description'])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thought = None
        self.__update_required = False
        get_api().events.thought_activated.subscribe(self.__thought_activated)

    @pyqtSlot(str, str, bool, name="changed")
    def changed(self, title, description, save):
        if not self.__thought:
            return

        # update thought model
        self.__thought.title = title
        self.__thought.description = description

        # notify thought was changed
        get_api().events.thought_changing.notify(self.__thought)

        # save changes if required or postpone it for later
        if save:
            self.__update_thought()
        else:
            self.__update_required = True

    def __thought_activated(self, thought):
        if self.__update_required:
            self.__update_thought()

        self.__thought = None
        self.activated.emit(thought.title,
                            thought.description or "")
        self.__thought = thought


    def __update_thought(self):
        if self.__thought:
            get_api().brain.storage.update(self.__thought)
            get_api().events.message.notify(("Updated", True))
            self.__update_required = False
