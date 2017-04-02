from api.commands import Command


class CreateCommand(Command):
    NAME = "create"

    def __init__(self):
        self.__created = None

    def execute(self, api):
        self.__created = api.database.create()

    def revert(self, api):
        api.database.delete(self.__created)


class DeleteCommand(Command):
    NAME = "delete"

    def __init__(self):
        self.__deleted = None

    def execute(self, api):
        self.__deleted = api.database.delete()

    def revert(self, api):
        api.database.add(self.__deleted)
