from abc import abstractmethod, ABCMeta
from collections import namedtuple

from sarasvati import get_api
from sarasvati.brain import Thought
from sarasvati.brain.link import LinkType


class Command(metaclass=ABCMeta):
    """Provides basic command interface"""
    def __init__(self):
        """Initializes new instance of the Command class."""
        self._api = get_api()
        self._events = self._api.events

    @abstractmethod
    def execute(self):
        """Executes command"""
        pass

    @abstractmethod
    def revert(self):
        """Reverts changes"""
        pass

    # noinspection PyMethodMayBeStatic
    def can_execute(self):
        """
        Checks if command can be executed
        :rtype: bool
        :return: True - if command can be executed, otherwise False
        """
        return True

    def on_completed(self):
        """Calls when execution is completed"""
        pass

    @property
    def view(self):
        """Return human readable representation of the command."""
        class_name = self.__class__.__name__
        return ''.join(map(lambda x: x if x.islower() else " " + x, class_name)).strip().replace(" Command", "")


class CommandException(Exception):
    pass


class Transaction:
    pass


CommandResult = namedtuple("CommandResult", ["value", "message"])


class ActivateCommand(Command):
    def __init__(self, thought):
        super().__init__()
        self.__thought = thought
        self.__prev = None

    def execute(self):
        self.__prev = self._api.brain.state.active_thought
        self._api.brain.state.activate(self.__thought)

    def revert(self):
        self._api.brain.state.activate(self.__prev)

    @property
    def view(self):
        return "Activate '{}' thought".format(self.__thought.title)


class CreateCommand(Command):
    def __init__(self, title, key=None):
        super().__init__()
        self.__created = None
        self.__title = title
        self.__key = key

    def execute(self):
        self.__created = Thought(self.__title, key=self.__key)
        self._api.brain.storage.add(self.__created)
        return self.__created

    def revert(self):
        self._api.brain.storage.remove(self.__created)

    @property
    def view(self):
        return "Create '{}' thought".format(self.__created.title)


class DeleteCommand(Command):
    def __init__(self, thought):
        super().__init__()
        self.__thought = thought
        self.__links = []

    def execute(self):
        # cache links to be removed
        for thought in self.__thought.links.all:
            self.__links.append(thought.links.to(self.__thought))

        # remove thought
        self._api.brain.storage.remove(self.__thought)

    def revert(self):
        # add thought back to storage
        self._api.brain.storage.add(self.__thought)

        # restore links
        for link in self.__links:
            link.source.links.add_link(link)
            self._api.brain.storage.update(link.source)

        self._api.brain.storage.update(self.__thought)

    @property
    def view(self):
        return "Delete '{}' thought".format(self.__thought.title)


class SetTitleCommand(Command):
    def __init__(self, thought, title):
        super().__init__()
        self.__thought = thought
        self.__new = title
        self.__old = thought.title

    def execute(self):
        self.__thought.title = self.__new

    def revert(self):
        self.__thought.title = self.__old

    def on_completed(self):
        self._api.brain.storage.update(self.__thought)

    @property
    def view(self):
        return "Set title to '{}' for '{}' thought".format(self.__new, self.__thought.title)


class SetDescriptionCommand(Command):
    def __init__(self, thought, description):
        super().__init__()
        self.__thought = thought
        self.__new = description
        self.__old = thought.description

    def execute(self):
        self.__thought.description = self.__new

    def revert(self):
        self.__thought.description = self.__old

    def on_completed(self):
        self._api.brain.storage.update(self.__thought)

    @property
    def view(self):
        return "Set description to '{}' for '{}' thought".format(self.__new, self.__thought.title)


class LinkCommand(Command):
    def __init__(self, source, destination, kind):
        super().__init__()
        self.__source = source
        self.__destination = destination
        self.__kind = kind

    def execute(self):
        source = self.__source.links.add(self.__destination, self.__kind)
        destination = self.__destination.links.add(self.__source, LinkType.opposite(self.__kind))
        return [source, destination]

    def revert(self):
        self.__source.links.remove(self.__destination)
        self.__destination.links.remove(self.__source)

    def on_completed(self):
        self._api.brain.storage.update(self.__source)
        self._api.brain.storage.update(self.__destination)

    @property
    def view(self):
        return "Link '{}' to '{}' as {}".format(self.__source.title, self.__destination.title, self.__kind)
