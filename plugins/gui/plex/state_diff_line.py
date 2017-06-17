class PlexStateDiffLine:
    def __init__(self, thought, old_state, new_state):
        """
        Initializes new instance of the PlexStateDiffLine class
        :param thought: Thought
        :param old_state: Old state
        :param new_state: New state
        """
        self.thought = thought
        self.old_state = old_state
        self.new_state = new_state

    def __eq__(self, other):
        """
        Checks equality of two instances
        :param other: Instance to check with
        :return: True - equal, otherwise False
        """
        return self.thought == other.thought and \
            self.old_state == other.old_state and \
            self.new_state == other.new_state

    def __repr__(self):
        return "<{}/{}->{}>".format(self.thought.title, self.old_state, self.new_state)
