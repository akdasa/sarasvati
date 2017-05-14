import pytest

from api.brain import Brain
from api.brain.model import IdentityComponent
from api.brain.thought import DefinitionComponent, LinksComponent
from api.commands import Command
from sarasvati.storage_local import LocalStorage


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
    storage = LocalStorage(None)
    return Brain(storage)


@pytest.fixture
def command():
    return DummyCommand()


def _get_component(key):
    options = {
        IdentityComponent.COMPONENT_NAME: IdentityComponent,
        DefinitionComponent.COMPONENT_NAME: DefinitionComponent,
        LinksComponent.COMPONENT_NAME: LinksComponent}
    res = options.get(key, None)
    if res:
        return res()
    return None


@pytest.fixture
def serialization_options():
    return {
        "get_component": _get_component
    }
