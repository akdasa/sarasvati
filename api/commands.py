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

    def on_completed(self):
        pass


class CommandApi:
    def __init__(self, brain):
        self.__active_thought = None
        self.__brain = brain

    @property
    def brain(self):
        return self.__brain
