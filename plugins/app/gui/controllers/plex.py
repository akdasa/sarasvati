from PyQt5.QtCore import QObject, pyqtSignal, QVariant

from ..plex import Plex, PlexLayout
from sarasvati import get_api


class PlexController(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.__plex = Plex()
        self.__layout = PlexLayout()
        self.__thought = None

        get_api().events.activated.subscribe(self.__thought_activated)
        get_api().events.thought_changed.subscribe(self.__thought_changed)
        get_api().events.thought_deleted.subscribe(self.__brain_changed)
        get_api().events.thought_created.subscribe(self.__brain_changed)
        get_api().events.thought_changing.subscribe(self.__thought_changing)
        #get_api().events.brain_changed.subscribe(self.__brain_changed)

    command = pyqtSignal(QVariant, arguments=['command'])

    def __change_state(self, thought):
        new_state = self.__plex.activate(thought)
        actions = self.__layout.change_to(new_state, True)

        for cmd in actions:
            v = {"cmd": cmd.name, "key": cmd.thought.key}

            if cmd.name == "add":
                v["title"] = cmd.thought.title
                v["x"] = cmd.data["pos"][0]
                v["y"] = cmd.data["pos"][1]
            if cmd.name == "move":  # or cmd.name == "set_pos_to":
                v["x"] = cmd.data[0]
                v["y"] = cmd.data[1]
            self.command.emit(QVariant(v))

        if thought:
            for links in thought.links.all:
                self.command.emit({"cmd": "link", "from": thought.key, "to": links.key,
                                   "ft": thought.title, "tt": links.title})

    def __thought_activated(self, thought):
        self.__change_state(thought)
        self.__thought = thought

    def __thought_changed(self, thought):
        self.command.emit({"cmd": "change", "key": thought.key, "title": thought.title})
        self.__change_state(self.__thought)

    def __thought_changing(self, data):
        emit_data = data.copy()
        emit_data["cmd"] = "change"
        self.command.emit(emit_data)

    def __brain_changed(self, thought):
        self.__change_state(self.__thought)
