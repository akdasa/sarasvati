from .thought_state import PlexThoughtState


class PlexState:
    def __init__(self):
        """
        Initializes new instance of the PlexState class
        """
        self.__state = []

    def add(self, thought, state):
        """
        Adds thought using specified state
        :param thought: Thought
        :param state: State
        """
        self.__state.append(PlexThoughtState(thought, state))

    def get_state(self):
        """
        Returns state
        :return: Array of PlexThoughtState
        """
        return self.__state.copy()

    def by_state(self, state):
        """
        Returns array of thoughts using specified state
        :param state: State
        :return: Array of thoughts
        """
        return [e.thought for e in self.__state if e.state == state]

    def by_key(self, key):
        # TODO: refactor using next()
        """
        Returns state by specified thought key
        :param key: Thought key
        :return: PlexThoughtState
        """
        for ptp in self.__state:
            if ptp.thought.key == key:
                return ptp
