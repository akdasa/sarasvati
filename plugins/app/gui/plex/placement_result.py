from math import sqrt, pow


class PlacementResult:
    def __init__(self, data):
        """Initializes new instance of the PlacementResult class."""
        self.__data = data

    def position(self, thought):
        """
        Gets position of specified thought
        :type thought: Thought
        :param thought: Thought to get position for
        :return:
        """
        if not thought:
            raise ValueError("Thought is not specified to get position for")
        return self.__data.get(thought.key, None)

    def distance(self, one, two):
        """
        Returns distance between two thoughts
        :param one: First thought
        :param two: Second thought
        :return: Distance, otherwise None
        """
        pos_one = self.position(one)
        pos_two = self.position(two)

        if pos_one and pos_two:
            return sqrt(
                pow(pos_two[0] - pos_one[0], 2) +
                pow(pos_two[1] - pos_one[1], 2))
