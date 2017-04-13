import uuid

from api.commands import CommandApi
from api.interfaces import Composite, Component


class Model(Composite):
    """
    Model is a basic entity to create other entities from.
    Contains IdentityComponent and SerializationComponent.
    """
    def __init__(self, components=None):
        """Initializes new instance of the Model class."""
        super().__init__(components=[
            IdentityComponent(),
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
    def serialization(self):
        """
        Returns serialization component
        :rtype: SerializationComponent
        :return: Serialization component
        """
        return self.get_component(SerializationComponent.COMPONENT_NAME)

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


class SerializationComponent(Component):
    COMPONENT_NAME = "serialization"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__model = None

    def serialize(self, options=None):
        result = {}
        for component in self.__model.components:
            if component.name == self.COMPONENT_NAME:
                continue

            data = component.serialize(options)
            if data:
                result[component.name] = data
        return result

    def deserialize(self, data, options=None):
        for key in data.keys():
            component_class = options.get(key, None)
            component_data = data[key]
            model_has_component = self.__model.has_component(key)

            if component_class and model_has_component:
                component = self.__model.get_component(key)
                component.deserialize(component_data, options)
            elif component_class:
                component = component_class()
                component.deserialize(component_data, options)
                self.__model.add_component(component)

    def on_added(self, composite):
        self.__model = composite


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

    def serialize(self, options=None):
        return {"title": self.title,
                "description": self.description}

    def deserialize(self, data, options=None):
        self.title = data.get("title", None)
        self.description = data.get("description", None)


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

    def on_added(self, composite):
        self.__source = composite

    def serialize(self, options=None):
        result = []
        for key in self.__links:
            l = self.__links[key]
            result.append({"key": l.destination.key, "kind": l.kind})
        if len(result) == 0:
            return None
        return result

    def deserialize(self, data, options=None):
        # increase depth level to avoid deserialization of
        # whole database
        depth_options = options.copy() #(options or {"depth": 0}).copy()
        if "depth" not in depth_options:
            depth_options["depth"] = 0
        else:
            depth_options["depth"] += 1

        # get storage to retrieve linked thoughts
        storage = options.get("storage", None)
        if not storage:
            raise Exception("No 'storage' specified to load linked thoughts")

        # deserialize each link
        for link in data:
            thought = storage.get(link["key"], depth_options)
            if thought is None:
                raise Exception("No link '{}' found".format(link["key"]))
            self.add(thought, link["kind"])

    def __get_links_of_kind(self, kind):
        links = filter(lambda x: x.kind == kind, self.__links.values())
        thoughts = map(lambda x: x.destination, links)
        return list(thoughts)


class Brain(Composite):
    def __init__(self, storage):
        """
        Initializes new instance of Brain class
        :type storage: Storage
        :param storage: Storage
        """
        super().__init__()
        self.__storage = storage
        self.add_components([
            BrainCommandsComponent(),
            BrainSearchComponent(self.__storage),
            BrainStatsComponent(self.__storage)
        ])

    @property
    def commands(self):
        """
        Returns commands component
        :rtype: BrainCommandsComponent
        :return: Commands component
        """
        return self.get_component(BrainCommandsComponent.COMPONENT_NAME)

    @property
    def search(self):
        """
        Returns search component
        :rtype: BrainSearchComponent
        :return: Search component
        """
        return self.get_component(BrainSearchComponent.COMPONENT_NAME)

    @property
    def stats(self):
        """
        Returns commands component
        :rtype: BrainStatsComponent
        :return: Stats component
        """
        return self.get_component(BrainStatsComponent.COMPONENT_NAME)


class BrainStatsComponent(Component):
    """Provides interface to see statistics of the brain"""
    COMPONENT_NAME = "stats"

    def __init__(self, storage):
        """
        Initializes new instance of the BrainStatsComponent class
        :type storage: Storage
        :param storage: Storage of the thoughts
        """
        super().__init__(self.COMPONENT_NAME)
        self.__storage = storage

    @property
    def thoughts_count(self):
        """
        Returns count of thoughts in brain
        :rtype: int
        :return: Count of thoughts
        """
        return self.__storage.count()


class BrainSearchComponent(Component):
    """Provides interface to search thought in brain"""
    COMPONENT_NAME = "search"

    def __init__(self, storage):
        """
        Initializes new instance of the BrainSearchComponent class
        :type storage: Storage
        :param storage: Storage of thoughts
        """
        super().__init__(self.COMPONENT_NAME)
        self.__storage = storage

    def by_query(self, query):
        """
        Returns result of search using specified query
        :param query: Query
        :return: Result
        """
        return self.__storage.search(query)

    def by_id(self, key):
        """
        Returns thought
        :param key: Identity of thought
        :return: Thought
        """
        result = self.by_query({
            "field": "identity.key",
            "operator": "=",
            "value": key
        })
        return result[0] if len(result) != 0 else None

    def by_title(self, title, operator="eq"):
        """
        Returns list of thoughts found by title
        :param title: Title
        :param operator: Operator (eq, contains) to test title with.
        :return: List of thoughts
        """
        return self.by_query({
            "field": "definition.title",
            "operator": operator,
            "value": title
        })

    def in_description(self, value, operator="~~"):
        return self.by_query({
            "field": "definition.description",
            "operator": operator,
            "value": value
        })


class BrainCommandsComponent(Component):
    """Provides interface to manipulate brain with commands"""
    COMPONENT_NAME = "commands"

    def __init__(self):
        """
        Initializes new instance of the BrainCommandsComponent class.
        :type api: BrainApi
        :param api: Api to manipulate brain with.
        """
        super().__init__(self.COMPONENT_NAME)
        self.__commands = []

    def execute(self, command):
        """
        Executes specified command
        :type command: Command
        :param command: Command to execute
        :return: Result of execution
        :raises BrainCommandException: If command was already executed
        :raises BrainCommandException: If some exception raised while executing command
        """
        if self.__is_executed(command):
            raise Exception("Command already executed", command)
        self.__commands.append(command)
        try:
            return command.execute()
        except Exception as ex:
            raise Exception("Error while executing command", command) from ex

    def revert(self):
        """
        Reverts changes of last executed command back
        :raises BrainCommandException: If nothing to undo
        """
        if len(self.__commands) <= 0:
            raise Exception("Nothing to undo")
        command = self.__commands.pop()
        return command.revert()

    def __is_executed(self, command):
        """Is specified command was executed previously?"""
        return command in self.__commands
