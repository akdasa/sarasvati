import pytest

from plugins.storage import LocalStorage
from sarasvati.brain import Brain
from sarasvati.commands import Command


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
    return Brain(LocalStorage(None))


@pytest.fixture
def command():
    return DummyCommand()

