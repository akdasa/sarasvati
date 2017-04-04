from api.commands import Command


class ActivateThoughtCommand(Command):
    def __init__(self, thought):
        self.__thought = thought
        self.__prev = None

    def execute(self, api):
        self.__prev = api.active_thought
        api.active_thought = self.__thought

    def revert(self, api):
        api.active_thought = self.__prev


class CreateCommand(Command):
    def __init__(self, title):
        self.__created = None
        self.__title = title

    def execute(self, api):
        self.__created = api.database.create()
        self.__created.title = self.__title
        return self.__created

    def revert(self, api):
        api.database.delete(self.__created)


class DeleteCommand(Command):
    def __init__(self, thought):
        self.__thought = thought

    def execute(self, api):
        api.database.delete(self.__thought)

    def revert(self, api):
        api.database.add(self.__thought)


class SetTitleCommand(Command):
    def __init__(self, thought, title):
        if thought is None:
            raise ValueError("Thought is none")
        self.__thought = thought
        self.__new_title = title
        self.__old_title = thought.title

    def execute(self, api):
        self.__thought.title = self.__new_title

    def revert(self, api):
        self.__thought.title = self.__old_title


class SetDescriptionCommand(Command):
    def __init__(self, thought, description):
        if thought is None:
            raise ValueError("Thought is none")
        self.__thought = thought
        self.__new_description = description
        self.__old_description = thought.description

    def execute(self, api):
        self.__thought.description = self.__new_description

    def revert(self, api):
        self.__thought.description = self.__old_description

