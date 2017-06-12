import pytest

from plugins.storage import LocalStorage
from sarasvati.brain import Brain
from sarasvati.brain.model import IdentityComponent
from sarasvati.brain.thought import DefinitionComponent, LinksComponent
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


@pytest.fixture
def serialization_options():
    return {
        "get_component": _get_component
    }


def _get_component(key):
    options = {
        IdentityComponent.COMPONENT_NAME: IdentityComponent,
        DefinitionComponent.COMPONENT_NAME: DefinitionComponent,
        LinksComponent.COMPONENT_NAME: LinksComponent}
    res = options.get(key, None)
    if res:
        return res()
    return None

