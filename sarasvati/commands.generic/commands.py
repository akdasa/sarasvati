from api.commands import Command


class ActivateCommand(Command):
    def __init__(self, api, thought):
        super().__init__(api)
        self.__thought = thought
        self.__prev = None

    def execute(self):
        self.__prev = self._api.active_thought
        self._api.active_thought = self.__thought

    def revert(self):
        self._api.active_thought = self.__prev


class CreateCommand(Command):
    def __init__(self, api, title):
        super().__init__(api)
        self.__created = None
        self.__title = title

    def execute(self):
        self.__created = self._api.database.create()
        self.__created.title = self.__title
        return self.__created

    def revert(self):
        self._api.database.delete(self.__created)


class DeleteCommand(Command):
    def __init__(self, api, thought):
        super().__init__(api)
        self.__thought = thought

    def execute(self):
        self._api.database.delete(self.__thought)

    def revert(self):
        self._api.database.add(self.__thought)


class SetTitleCommand(Command):
    def __init__(self, api, thought, title):
        super().__init__(api)
        if thought is None:
            raise ValueError("Thought is none")
        self.__thought = thought
        self.__new_title = title
        self.__old_title = thought.title

    def execute(self):
        self.__thought.title = self.__new_title

    def revert(self):
        self.__thought.title = self.__old_title


class SetDescriptionCommand(Command):
    def __init__(self, api, thought, description):
        super().__init__(api)
        if thought is None:
            raise ValueError("Thought is none")
        self.__thought = thought
        self.__new_description = description
        self.__old_description = thought.description

    def execute(self):
        self.__thought.description = self.__new_description

    def revert(self):
        self.__thought.description = self.__old_description
