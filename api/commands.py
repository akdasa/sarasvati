class Command:
    def execute(self, api):
        pass

    def revert(self, api):
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


