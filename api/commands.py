class Command:
    NAME = None

    def execute(self, api):
        pass

    def revert(self, api):
        pass


class CommandApi:
    def __init__(self, database):
        self.__database = database

    @property
    def database(self):
        return self.__database
