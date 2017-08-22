class PlexThoughtState:
    """
    Represents thought state in the plex
    """
    def __init__(self, thought, state):
        """
        Initializes new instance of the PlexThoughtState class
        :param thought: Thought
        :param state: state
        """
        self.thought = thought
        self.state = state

    def __repr__(self):
        """
        Returns string representation of the instance
        :return: string
        """
        return str(self.thought) + " [" + self.state + "]"
