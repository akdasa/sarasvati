from api.commands import Command
from api.models import Thought


class ActivateCommand(Command):
    def __init__(self, api, thought):
        super().__init__(api)
        self.__thought = thought
        self.__prev = None

    def execute(self):
        self.__prev = self._api.brain.state.active_thought
        self._api.brain.state.activate(self.__thought)

    def revert(self):
        self._api.brain.state.activate(self.__prev)


class CreateCommand(Command):
    def __init__(self, api, title):
        super().__init__(api)
        self.__created = None
        self.__title = title

    def execute(self):
        self.__created = Thought(self.__title)
        self._api.storage.add(self.__created)
        return self.__created

    def revert(self):
        self._api.storage.delete(self.__created)


class DeleteCommand(Command):
    def __init__(self, api, thought):
        super().__init__(api)
        self.__thought = thought

    def execute(self):
        self._api.storage.delete(self.__thought)

    def revert(self):
        self._api.storage.add(self.__thought)


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

    def on_completed(self):
        self._api.brain.storage.update(self.__thought)


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

    def on_completed(self):
        self._api.brain.storage.update(self.__thought)


class LinkCommand(Command):
    def __init__(self, api, source, destination, kind):
        super().__init__(api)
        self.__source = source
        self.__destination = destination
        self.__kind = kind

    def execute(self):
        self.__source.links.add(self.__destination, self.__kind)

    def revert(self):
        self.__source.links.remove(self.__destination)

    def on_completed(self):
        self._api.brain.storage.update(self.__source)
