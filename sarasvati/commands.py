from abc import abstractmethod, ABCMeta
from collections import namedtuple

from sarasvati import get_api


class Command(metaclass=ABCMeta):
    """Provides basic command interface"""
    def __init__(self):
        """Initializes new instance of the Command class."""
        self._api = get_api()

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


CommandResult = namedtuple("CommandResult", ["value", "message"])