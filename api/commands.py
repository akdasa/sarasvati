from abc import abstractmethod, ABCMeta
from api import get_api


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


class CommandException(Exception):
    pass
