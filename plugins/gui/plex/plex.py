from .state import PlexState


class Plex:
    """
    Plex is a slice of the brain
    """
    def __init__(self):
        self.__state = None

    def activate(self, thought):
        """
        Activate thought
        :rtype: PlexState
        :type thought: Thought
        :param thought: Thought
        :return: State of the plex
        """
        self.__state = PlexState()

        if thought:
            self.__state.add(thought, "root")
            links = thought.links.all
            for link_key in links:
                link = links[link_key]
                self.__state.add(link.destination, link.kind)
        return self.__state

    @property
    def state(self):
        return self.__state
