from sarasvati.brain import Thought
from sarasvati.commands import Command


class ActivateCommand(Command):
    def __init__(self, thought):
        super().__init__()
        self.__thought = thought
        self.__prev = None

    def execute(self):
        self.__prev = self._api.brain.state.active_thought
        self._api.brain.state.activate(self.__thought)

    def revert(self):
        self._api.brain.state.activate(self.__prev)

    @property
    def view(self):
        return "Activate '{}' thought".format(self.__thought.title)


class CreateCommand(Command):
    def __init__(self, title, key=None):
        super().__init__()
        self.__created = None
        self.__title = title
        self.__key = key

    def execute(self):
        self.__created = Thought(self.__title, key=self.__key)
        self._api.brain.storage.add(self.__created)
        return self.__created

    def revert(self):
        self._api.brain.storage.remove(self.__created)

    @property
    def view(self):
        return "Create '{}' thought".format(self.__created.title)


class DeleteCommand(Command):
    def __init__(self, thought):
        super().__init__()
        self.__thought = thought

    def execute(self):
        self._api.brain.storage.remove(self.__thought)

    def revert(self):
        self._api.brain.storage.add(self.__thought)

    @property
    def view(self):
        return "Delete '{}' thought".format(self.__thought.title)


class SetTitleCommand(Command):
    def __init__(self, thought, title):
        super().__init__()
        self.__thought = thought
        self.__new = title
        self.__old = thought.title

    def execute(self):
        self.__thought.title = self.__new

    def revert(self):
        self.__thought.title = self.__old

    def on_completed(self):
        self._api.brain.storage.update(self.__thought)

    @property
    def view(self):
        return "Set title to '{}' for '{}' thought".format(self.__new, self.__thought.title)


class SetDescriptionCommand(Command):
    def __init__(self, thought, description):
        super().__init__()
        self.__thought = thought
        self.__new = description
        self.__old = thought.description

    def execute(self):
        self.__thought.description = self.__new

    def revert(self):
        self.__thought.description = self.__old

    def on_completed(self):
        self._api.brain.storage.update(self.__thought)

    @property
    def view(self):
        return "Set description to '{}' for '{}' thought".format(self.__new, self.__thought.title)


class LinkCommand(Command):
    def __init__(self, source, destination, kind):
        super().__init__()
        self.__source = source
        self.__destination = destination
        self.__kind = kind

    def execute(self):
        source = self.__source.links.add(self.__destination, self.__kind)
        destination = self.__destination.links.add(self.__source, self.__back(self.__kind))
        return [source, destination]

    def revert(self):
        self.__source.links.remove(self.__destination)
        self.__destination.links.remove(self.__source)

    def on_completed(self):
        self._api.brain.storage.update(self.__source)
        self._api.brain.storage.update(self.__destination)

    @property
    def view(self):
        return "Link '{}' to '{}' as {}".format(self.__source.title, self.__destination.title, self.__kind)

    @staticmethod
    def __back(kind):
        return {"child": "parent", "parent": "child", "reference": "reference"}.get(kind)
