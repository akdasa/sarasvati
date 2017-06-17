from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from plugins.gui.plex import Plex, PlexStateDiff, PlexLayout
from sarasvati import get_api
from sarasvati.brain import Thought


class PlexController(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.__plex = Plex(None)
        self.__differ = PlexStateDiff()
        self.__layout = PlexLayout()
        self.__actions = None

        get_api().events.thought_activated.subscribe(self.__thought_activated)

    commandResult = pyqtSignal(dict, arguments=['command'])

    @pyqtSlot(str, name="activate")
    def activate(self, key):
        thought = get_api().brain.search.by_key(key)
        new_state = self.__plex.activate(thought)
        self.__actions = self.__layout.change_to(new_state)
        self.__execute()

    def __execute(self):
        # Sum two arguments and emit a signal
        for cmd in self.__actions:
            v = {"cmd": cmd.name, "key": cmd.thought.key}

            if cmd.name == "add":
                v["title"] = cmd.thought.title
            elif cmd.name == "move_to" and not isinstance(cmd.data, Thought):
                v["x"] = cmd.data[0]
                v["y"] = cmd.data[1]
            elif cmd.name == "move_to" and isinstance(cmd.data, Thought):
                for cmd2 in self.__actions:
                    if cmd2.thought == cmd.data and cmd2.name == "move_to":
                        v["x"] = cmd2.data[0]
                        v["y"] = cmd2.data[1]
            elif cmd.name == "delete":
                pass
            self.commandResult.emit(v)

    def __thought_activated(self, thought):
        self.activate(thought.key)
