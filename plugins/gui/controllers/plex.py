from PyQt5.QtCore import QObject, pyqtSignal

from plugins.gui.plex import Plex, PlexLayout
from sarasvati import get_api


class PlexController(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.__plex = Plex()
        self.__layout = PlexLayout()

        get_api().events.thought_activated.subscribe(self.__thought_activated)

    command = pyqtSignal(dict, arguments=['command'])

    def __change_state(self, thought):
        new_state = self.__plex.activate(thought)
        actions = self.__layout.change_to(new_state)

        for cmd in actions:
            v = {"cmd": cmd.name, "key": cmd.thought.key}

            if cmd.name == "add":
                v["title"] = cmd.thought.title
            if cmd.name == "move_to" or cmd.name == "set_pos_to":
                v["x"] = cmd.data[0]
                v["y"] = cmd.data[1]
            self.command.emit(v)

        if thought:
            for links in thought.links.all:
                self.command.emit({"cmd": "link", "from": thought.key, "to": links.key,"ft": thought.title, "tt": links.title})

    def __thought_activated(self, thought):
        self.__change_state(thought)
