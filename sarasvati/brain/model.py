import uuid

from sarasvati.models import Composite, Component


class Model(Composite):
    """
    Model is a basic entity to create other entities from.
    Contains IdentityComponent and SerializationComponent.
    """
    def __init__(self, key=None, components=None):
        """
        Initializes new instance of the Model class.
        :param key: Identity key
        :param components: Array of components to construct Model from
        """
        super().__init__(components=[
            IdentityComponent(key),
            SerializationComponent()
        ])
        if components is not None:
            self.add_components(components)

    @property
    def key(self):
        """
        Gets identification value of the model.
        :rtype: str
        """
        return self.identity.key

    @property
    def identity(self):
        """
        Returns identity component of the model.
        :rtype: IdentityComponent
        :return: Identity component
        """
        return self.get_component(IdentityComponent.COMPONENT_NAME)

    @property
    def serialization(self):
        """
        Returns serialization component of the model.
        :rtype: SerializationComponent
        :return: Serialization component
        """
        return self.get_component(SerializationComponent.COMPONENT_NAME)

    def __repr__(self):
        """Return string representation of model."""
        return "<Model:" + self.key + ">"


class IdentityComponent(Component):
    COMPONENT_NAME = "identity"

    def __init__(self, key=None):
        """
        Initializes new instance of the IdentityComponent class.
        :type key: str
        :param key: Id value.
        """
        super().__init__(self.COMPONENT_NAME)
        self.__key = key or uuid.uuid4().hex

    @property
    def key(self):
        """
        Return identity value
        :rtype: str
        :return: Identity
        """
        return self.__key

    @key.setter
    def key(self, value):
        """
        Sets identity value
        :type value: str
        :param value: Identity
        """
        self.__key = value

    def serialize(self, options=None):
        return {"key": self.__key}

    def deserialize(self, data, options=None):
        if "key" not in data:
            raise Exception("Required 'key' does not present in data")
        self.__key = data.get("key", None)


class SerializationComponent(Component):
    COMPONENT_NAME = "serialization"
    __GET_COMPONENT = "get_component"

    def __init__(self):
        """
        Initializes new instance of the SerializationComponent class
        """
        super().__init__(self.COMPONENT_NAME)
        self.__model = None

    def serialize(self, options=None):
        """
        Serializes object
        :type options: dict
        :rtype: dict
        :param options: User specified options
        :return: Dictionary
        """
        result = {}
        for component in self.__model.components:
            if component.name == self.COMPONENT_NAME:
                continue  # do not serialize myself

            data = component.serialize(options)
            if data:
                result[component.name] = data
        return result

    def deserialize(self, data, options=None):
        """
        Deserialize specified data into model
        :param data: Data to deserialize from
        :param options: User specified options
        """
        get_component = options.get(self.__GET_COMPONENT, None)
        if not get_component:
            raise Exception("No '{}' specified".format(self.__GET_COMPONENT))

        for key in data.keys():
            component_data = data[key]

            if self.__model.has_component(key):
                component = self.__model.get_component(key)
                component.deserialize(component_data, options)
            else:  # create new component if not exist
                component = get_component(key)
                if not component:
                    raise Exception("No component provided for {} by '{}'".format(key, self.__GET_COMPONENT))
                component.deserialize(component_data, options)
                self.__model.add_component(component)

    def on_added(self, composite):
        self.__model = composite
