import pytest

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
def brain(api):
    return api.brain


@pytest.fixture
def command():
    return DummyCommand()


@pytest.fixture
def command2():
    return DummyCommand()
