from sarasvati.exceptions import SarasvatiException


class Serializer:
    def __init__(self):
        """Initializes new instance of the Serializer class."""
        self.__options = {}

    def register(self, name, serializer):
        """
        Registers serializer
        :type name: str
        :type serializer: Type[Serializer]
        :param name: name of serializer
        :param serializer: Serializer instance
        """
        self.__options[name] = serializer

    def serialize(self, model):
        """
        Serializes object into dictionary
        :rtype: dict
        :type model: Type[Composite]
        :param model: Model to serialize
        :return: Dictionary
        """
        result = {}
        for component in model.components:
            serializer = self.__serializer(component.name)
            data = serializer.serialize(component)
            if data:
                result[component.name] = data
        return result

    def deserialize(self, model, data):
        """
        Deserializes dictionary into model
        :type model: Type[Composite]
        :type data: dict
        :param model: Model to deserialize to
        :param data: Data to deserialize from
        :return: Deserialized model
        """
        for key in data.keys():
            component_data = data[key]
            serializer = self.__serializer(key)
            if model.has_component(key):
                component = model.get_component(key)
                serializer.deserialize(component_data, component)
            else:  # create new component if not exist
                component = serializer.deserialize(component_data)
                model.add_component(component)

        return model

    def __serializer(self, name):
        """Returns serializer by specified name"""
        serializer = self.__options.get(name, None)
        if not serializer:
            raise SarasvatiException("No serializer found for '{}'".format(name))
        return serializer
