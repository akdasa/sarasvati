import pytest

from api.brain import Brain
from api.brain.model import IdentityComponent
from api.brain.thought import DefinitionComponent, LinksComponent
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
