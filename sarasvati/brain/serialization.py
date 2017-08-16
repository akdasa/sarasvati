
class ComponentSerializer:
    def serialize(self, component):
        """
        Serializes component into dictionary.
        :type component: type[Component]
        :rtype: dict
        :param component: Component to serialize
        """
        pass

    def deserialize(self, data, component=None):
        """
        Deserialize component from dictionary
        :param data: Data to deserialize from.
        :param component: Component to deserialize to. Creates new if None specified.
        """
        pass
