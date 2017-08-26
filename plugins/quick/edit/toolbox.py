from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickItem

from sarasvati import get_api
from sarasvati.commands import Transaction, SetTitleCommand, SetDescriptionCommand


class QuickEditToolbox(QQuickItem):
    activated = pyqtSignal(str, str, bool, arguments=[
        'thought_title', 'thought_description', 'enabled'])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__thought = None  # active thought
        self.__update_required = False  # changes required to be saved

        self.__title = None
        self.__description = None

        self.__api = get_api()
        self.__events = self.__api.events
        self.__events.activating.subscribe(self.__before_activated)
        self.__events.activated.subscribe(self.__activated)
        self.__events.thought_changed.subscribe(self.__on_thought_changed)

    @pyqtSlot(str, str, name="changed")
    def __on_input_fields_changed(self, title, description):
        if not self.__thought:
            return
        self.__title = title
        self.__description = description
        self.__update_required = \
            self.__thought.title != title or \
            self.__thought.description != description

        self.__notify_changing(description, title)

    @pyqtSlot(str, name="create")
    def __on_create(self, kind):
        self.__update_thought()
        self.__api.execute("/c new as:{}".format(kind))

    def __notify_changing(self, description, title):
        self.__events.thought_changing.notify({
            "key": self.__thought.key,
            "title": title,
            "description": description})

    def __before_activated(self, thought):
        if self.__update_required:
            self.__update_thought()

    def __activated(self, thought):
        self.__thought = None
        if thought is not None:
            self.activated.emit(thought.title,
                                thought.description or "", True)
        else:
            self.activated.emit("", "", False)
        self.__thought = thought

    def __on_thought_changed(self, thought):
        if self.__thought == thought:  # activated thought changed
            self.activated.emit(thought.title, thought.description or "", True)

    def __update_thought(self):
        if self.__update_required is False:
            return

        t = Transaction()
        c1 = SetTitleCommand(self.__thought, self.__title)
        c2 = SetDescriptionCommand(self.__thought, self.__description)
        self.__api.execute(c1, t)
        self.__api.execute(c2, t)
        self.__api.events.message.notify(("'{}' updated".format(self.__thought.title), True))
        self.__update_required = False
