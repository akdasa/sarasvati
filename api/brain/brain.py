from api.commands import CommandException
from api.interfaces import Composite, Component


class Brain(Composite):
    """Provides interface to store and manipulate thoughts"""
    def __init__(self, storage):
        """
        Initializes new instance of Brain class
        :param storage: Storage to keep thoughts in
        """
        super().__init__()
        self.__storage = storage
        self.add_components([
            BrainCommandsComponent(),
            BrainSearchComponent(self.__storage),
            BrainStatsComponent(self.__storage),
            BrainStateComponent(),
            BrainStorageComponent(self.__storage)
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
        Returns statistics component
        :rtype: BrainStatsComponent
        :return: Stats component
        """
        return self.get_component(BrainStatsComponent.COMPONENT_NAME)

    @property
    def state(self):
        """
        Return state component
        :return: BrainStateComponent
        """
        return self.get_component(BrainStateComponent.COMPONENT_NAME)

    @property
    def storage(self):
        """
        Return storage component
        :return: BrainStorageComponent
        """
        return self.get_component(BrainStorageComponent.COMPONENT_NAME)


class BrainStatsComponent(Component):
    """Provides interface to see statistics of the brain"""
    COMPONENT_NAME = "stats"

    def __init__(self, storage):
        """
        Initializes new instance of the BrainStatsComponent class
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
        """
        super().__init__(self.COMPONENT_NAME)
        self.__commands = []

    def execute(self, command):
        """
        Executes specified command
        :type command: Command
        :param command: Command to execute
        :return: Result of execution
        :raises Exception: If command was already executed
        :raises Exception: If some exception raised while executing command
        """
        if self.__is_executed(command):
            raise Exception("Command already executed", command)
        self.__commands.append(command)
        try:
            if not command.can_execute():
                raise CommandException("Command can not be executed")
            result = command.execute()
            command.on_completed()
            return result
        except Exception as ex:
            raise Exception("Error while executing command", command) from ex

    def revert(self):
        """
        Reverts changes of last executed command back
        :raises Exception: If nothing to undo
        """
        if len(self.__commands) <= 0:
            raise Exception("Nothing to undo")
        command = self.__commands.pop()
        result = command.revert()
        command.on_completed()
        return result

    def __is_executed(self, command):
        """Is specified command was executed previously?"""
        return command in self.__commands


class BrainStateComponent(Component):
    COMPONENT_NAME = "state"

    def __init__(self):
        """
        Initializes new instance of the BrainStateComponent class.
        """
        super().__init__(self.COMPONENT_NAME)
        self.__active_thought = None

    def activate(self, thought):
        """
        Activates specified thought
        :param thought: Thought to be activated
        """
        self.__active_thought = thought

    @property
    def active_thought(self):
        """
        Returns active thought
        :return: Thought
        """
        return self.__active_thought


class BrainStorageComponent(Component):
    COMPONENT_NAME = "storage"

    def __init__(self, storage):
        super().__init__(self.COMPONENT_NAME)
        self.__storage = storage

    def add(self, thought):
        self.__storage.add(thought)

    def update(self, thought):
        self.__storage.update(thought)

    def remove(self, thought):
        self.__storage.remove(thought)
