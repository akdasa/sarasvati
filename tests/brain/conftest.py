import pytest

from api.brain import Brain
from api.commands import Command
from api.plugins import PluginManager, StoragePlugin


class DummyCommand(Command):
    def __init__(self):
        super().__init__()
        self.executed = False
        self.reverted = False

    def execute(self):
        self.executed = True

    def revert(self):
        self.reverted = True


@pytest.fixture
def brain():
    pm = PluginManager(categories={"storage": StoragePlugin})
    plugins = pm.get("storage")
    storage = plugins.get_storage()
    return Brain(storage)


@pytest.fixture
def command():
    return DummyCommand()
