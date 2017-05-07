from abc import abstractmethod, ABCMeta


class Command(metaclass=ABCMeta):
    """Provides basic command interface"""
    def __init__(self, api=None):
        """
        Initializes new instance of the Command class.
        :type api: CommandApi
        :param api: Api
        """
        self._api = api

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


class CommandApi:
    def __init__(self, brain):
        self.__brain = brain

    @property
    def brain(self):
        return self.__brain

    @staticmethod
    def get_one(lst):
        """Returns one element from list, otherwise raises exception"""
        lst_len = len(lst)
        if lst_len == 0:
            raise CommandException("Nothing found")
        elif lst_len > 1:
            raise CommandException("More than one entity found")
        else:
            return lst[0]


class CommandException(Exception):
    pass
