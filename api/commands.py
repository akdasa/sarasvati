from abc import abstractmethod


class Command:
    """Provides basic command interface"""
    @abstractmethod
    def execute(self, api):
        """
        Executes command
        :type api: CommandApi
        :param api: api object
        """
        pass

    @abstractmethod
    def revert(self, api):
        """
        Reverts changes
        :type api: CommandApi
        :param api: api object
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


