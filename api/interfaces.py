class Composite:
    def __init__(self, components: list=None):
        """
        Initializes new instance of the Composite class.
        :type components: List[Component]
        :param components: Components to create composite from.
        """
        self.__components = {}

        if components is not None:
            self.add_components(components)

    def has_component(self, component_name) -> bool:
        """
        Returns true if component already added, otherwise false
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
            raise Exception("Component '" + name + "' not found for " + str(self))
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
        Deserializes component from dictionary
        :param data: Data to deserialize from.
        :param options: Options
        """
        pass
