import pytest

from sarasvati.serialization import IdentityComponentSerializer, DefinitionComponentSerializer, LinksComponentSerializer
from sarasvati.serializer import Serializer


@pytest.fixture(name="storage")
def __storage(api):
    api.execute("/c Brain key:Brain")
    api.execute("/c Tasks parent:Brain key:Tasks")
    api.execute("/c Recipes parent:Brain key:Recipes")
    api.execute("/c Read 'Alice in wunderland' parent:Tasks key:Task1")
    api.execute("/c Cook cake parent:Tasks key:Task2")
    api.execute("/c Anthill cake parent:Recipes key:Recipe1")
    api.execute("/c Simple wounderful parent:Recipes key:Recipe2")
    api.execute("/c Party key:Party")
    api.execute("/c Guests parent:Party key:Guests")
    api.execute("/l Cook cake to:Party as:child")
    api.execute("/l Cook cake to:Anthill cake as:reference")

    api.storage.cache.clear()

    return api.storage


@pytest.fixture(name="serializer")
def __serializer():
    s = Serializer()
    s.register("identity", IdentityComponentSerializer())
    s.register("definition", DefinitionComponentSerializer())
    s.register("links", LinksComponentSerializer(storage=None))
    return s


@pytest.fixture(name="script")
def __script(api):
    def __impl_execute(cmds, clear_cache=False):
        for cmd in cmds:
            api.execute(cmd)
        if clear_cache:
            api.storage.cache.clear()
    return __impl_execute
