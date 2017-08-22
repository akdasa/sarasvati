from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickItem

from sarasvati import get_api
from sarasvati.commands import Transaction, SetTitleCommand, SetDescriptionCommand


class QuickEditToolbox(QQuickItem):
    activated = pyqtSignal(str, str, arguments=['thought_title', 'thought_description'])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thought = None
        self.__update_required = False
        self.__new_title = None
        self.__new_description = None

        self.__api = get_api()
        self.__changing = self.__api.events.thought_changing

        self.__api.events.thought_before_activated.subscribe(self.__thought_before_activated)
        self.__api.events.thought_activated.subscribe(self.__thought_activated)
        self.__api.events.thought_changed.subscribe(self.__thought_changed)

    @pyqtSlot(str, str, name="changed")
    def __on_input_fields_changed(self, title, description):
        if not self.__thought:
            return
        self.__new_title = title
        self.__new_description = description
        self.__update_required = \
            self.__thought.title != title or \
            self.__thought.description != description

        # notify thought is changing
        self.__changing.notify({
            "key": self.__thought.key,
            "title": title,
            "description": description})

    def __thought_before_activated(self, thought):
        if self.__update_required:
            self.__update_thought()

    def __thought_activated(self, thought):
        self.__thought = None
        if thought is not None:
            self.activated.emit(thought.title,
                                thought.description or "")
        else:
            self.activated.emit("", "")
        self.__thought = thought

    def __thought_changed(self, thought):
        if self.__thought == thought:
            self.activated.emit(thought.title,
                                thought.description or "")

    def __update_thought(self):
        if self.__thought is not None:
            t = Transaction()
            c1 = SetTitleCommand(self.__thought, self.__new_title)
            c2 = SetDescriptionCommand(self.__thought, self.__new_description)
            self.__api.execute(c1, t)
            self.__api.execute(c2, t)
            self.__api.events.message.notify(("Updated", True))
            self.__update_required = False
