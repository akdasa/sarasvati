from collections import namedtuple

from plugins.app.gui.plex.layout import PlexLayout
from .state import PlexState


class Plex:
    """Plex is a slice of the brain"""

    __result = namedtuple("PlexActivationResult", ["state", "actions"])

    def __init__(self):
        self.__thought = None
        self.__state = None
        self.__layout = PlexLayout()

    def activate(self, thought, full=False):
        """
        Activate thought
        :rtype: PlexActivationResult
        :type thought: Thought
        :param thought: Thought
        :return: State of the plex
        """
        self.__thought = thought
        self.__state = PlexState()
        actions = None

        if thought:
            self.__state.add(thought, "root")
            links = thought.links.all
            for link_key in links:
                link = links[link_key]
                self.__state.add(link.destination, link.kind)

            actions = self.__layout.change_to(self.__state, full)

        return self.__result(self.__state, actions)

    @property
    def state(self):
        return self.__state

    @property
    def layout(self):
        return self.__layout

    @property
    def thought(self):
        return self.__thought
