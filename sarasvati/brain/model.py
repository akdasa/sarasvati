import uuid


class Composite:
    def __init__(self, components=None):
        """
        Initializes new instance of the Composite class.
        :type components: list
        :param components: Components to create composite from.
        """
        self.__components = {}

        if components is not None:
            self.add_components(components)

    def has_component(self, component_name):
        """
        Returns true if component already added, otherwise false
        :rtype: bool
        :type component_name: str
        :param component_name: Name of the component
        :return: True if component already added, otherwise false
        """
        return component_name in self.__components.keys()

    def add_component(self, component):
        """
        Adds specified component
        :type component: Component
        :param component: Component to add
        """
        if self.has_component(component.name):
            raise Exception("Component '" + component.name + "' already exist")
        self.__components[component.name] = component
        if hasattr(component, "on_added"):
            component.on_added(self)

    def add_components(self, components):
        """
        Adds specified list of components
        :type components: List[Component]
        :param components: Array of components
        """
        for component in components:
            self.add_component(component)

    def get_component(self, name):
        """
        Returns component using specified name. Raises exception if no component found.
        :type name: str
        :param name: Name of the component
        :return: Component
        """
        if name not in self.__components.keys():
            raise Exception("Component '{}' not found for '{}'".format(name, str(self)))

        return self.__components[name]

    @property
    def components(self):
        """
        Returns list of components
        :return: Components
        """
        return self.__components.values()

    def __getattr__(self, item):
        return self.get_component(item)


class Component:
    """
    Provides interface for custom component.
    """
    def __init__(self, name):
        """
        Initializes new instance of the Component class.
        :type name: str
        :param name: Name of the component. Should be unique.
        """
        self.__component_name = name

    @property
    def name(self):
        """
        Returns name of the component.
        :return: Name
        """
        return self.__component_name

    def serialize(self, options=None):
        """
        Serializes component into dictionary.
        :type options: dict
        :rtype: dict
        :param options: Options
        """
        pass

    def deserialize(self, data, options=None):
        """
        Deserialize component from dictionary
        :param data: Data to deserialize from.
        :param options: Options
        """
        pass


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
            else:
                component = get_component(key)
                if not component:
                    raise Exception("No component provided for {} by '{}'".format(key, self.__GET_COMPONENT))
                component.deserialize(component_data, options)
                self.__model.add_component(component)

    def on_added(self, composite):
        self.__model = composite
