import uuid
from api.interfaces import Composite, Component


class Model(Composite):
    """
    Model is a basic entity to create other entities from.
    Contains IdentityComponent and SerializationComponent.
    """
    def __init__(self, components=None):
        """Initializes new instance of the Model class."""
        super().__init__(components=[
            IdentityComponent()
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

    def __repr__(self):
        """Return string representation of model."""
        return "<Model:" + self.key + ">"


class Thought(Model):
    def __init__(self, title=None, description=None):
        """
        Initializes new instance of the Thought class.
        :type description: str
        :type title: str
        :param title: Title of the thought
        :param description: Short description of the thought
        """
        super().__init__(components=[
            DefinitionComponent(title, description),
            LinksComponent(self)
        ])

    @property
    def title(self):
        """Gets title of thought."""
        return self.definition.title

    @title.setter
    def title(self, value):
        """Sets title of thought."""
        self.definition.title = value

    @property
    def description(self):
        """Gets short description of thought."""
        return self.definition.description

    @description.setter
    def description(self, value):
        """Sets description of thought."""
        self.definition.description = value

    @property
    def definition(self):
        """
        Returns definition component
        :rtype: DefinitionComponent
        :return: Definition component
        """
        return self.get_component(DefinitionComponent.COMPONENT_NAME)

    @property
    def links(self):
        """
        Returns links component
        :rtype: LinksComponent
        :return: Links component
        """
        return self.get_component(LinksComponent.COMPONENT_NAME)

    def __repr__(self):
        """Returns string representation of thought."""
        return "<Thought:" + str(self.key) + "/" + str(self.title) + ">"


class Link:
    def __init__(self, source, destination, kind):
        """
        Initializes new instance of the Link class.
        :type source: Thought
        :type destination: Thought
        :type kind: str
        :param source: Source
        :param destination: Destination
        :param kind: Kind of link
        """
        self.__source = source
        self.__destination = destination
        self.__kind = kind

    @property
    def source(self):
        return self.__source

    @property
    def destination(self):
        return self.__destination

    @property
    def kind(self):
        return self.__kind


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


class DefinitionComponent(Component):
    COMPONENT_NAME = "definition"

    def __init__(self, title=None, description=None):
        """
        Initializes new instance of the DefinitionComponent class
        :type title: str
        :type description: str
        :param title: Title
        :param description: Description
        """
        super().__init__(self.COMPONENT_NAME)
        self.__title = title
        self.__description = description

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value


class LinksComponent(Component):
    """
    Provides interface to link thoughts
    """
    COMPONENT_NAME = "links"
    __correct_kinds = ["child", "parent", "reference"]

    def __init__(self, source=None):
        """
        Initializes new instance of the LinksComponent class
        :type source: Thought
        :param source: Source
        """
        super().__init__(self.COMPONENT_NAME)
        self.__links = {}
        self.__source = source

    def add(self, destination, kind):
        """
        Adds link to destination thought
        :type destination: Thought
        :type kind: str
        :param destination: Destination
        :param kind: Kind of link: [child, parent, reference]
        :raises Exception: If link to specified thought already been added
        :raises ValueError: If kind is incorrect
        :rtype: Link
        :return: Link
        """
        if destination in self.__links:
            raise Exception("Link to specified thought already exist")
        if kind not in self.__correct_kinds:
            raise ValueError("Link kind is not correct: " + kind)
        if self.__source is destination:
            raise ValueError("Unable link thought to itself")
        link = Link(self.__source, destination, kind)
        self.__links[destination] = link
        return link

    def remove(self, destination):
        """
        Removes link to specified thought
        :type destination: Thought
        :param destination: Thought
        :raises Exception: If link to specified thought doesn't exist
        """
        if destination not in self.__links:
            raise Exception("Link to specified thought does not exist")
        del self.__links[destination]

    @property
    def all(self):
        return self.__links

    @property
    def count(self):
        """Returns count of links"""
        return len(self.__links)

    @property
    def children(self):
        """Returns children"""
        return self.__get_links_of_kind("child")

    @property
    def parents(self):
        """Returns parents"""
        return self.__get_links_of_kind("parent")

    @property
    def references(self):
        """Returns references"""
        return self.__get_links_of_kind("reference")

    def __get_links_of_kind(self, kind):
        links = filter(lambda x: x.kind == kind, self.__links.values())
        thoughts = map(lambda x: x.destination, links)
        return list(thoughts)

    def on_added(self, composite):
        self.__source = composite