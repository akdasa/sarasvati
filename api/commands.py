from abc import abstractmethod, ABCMeta


class Command(metaclass=ABCMeta):
    """Provides basic command interface"""
    def __init__(self, api):
        """
        Initializes new instance of the Command class.
        :type api: CommandApi
        :param api: Api
        """
        self._api = api

    @abstractmethod
    def execute(self):
        """
        Executes command
        """
        pass

    @abstractmethod
    def revert(self):
        """
        Reverts changes
        """
        pass


class CommandApi:
    def __init__(self, database):
        self.__database = database
        self.__active_thought = None

    @property
    def database(self):
        return self.__database

    @property
    def active_thought(self):
        return self.__active_thought

    @active_thought.setter
    def active_thought(self, value):
        self.__active_thought = value
