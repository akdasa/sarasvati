import pytest

from plugins.storage.local import LocalStorage
from sarasvati.brain import Thought
from sarasvati.serialization import IdentityComponentSerializer, DefinitionComponentSerializer, LinksComponentSerializer


@pytest.fixture(name="thought")
def __thought():
    return Thought("Root", key="Root")


@pytest.fixture(name="get_storage")
def __get_storage():
    def __get_storage(path):
        storage = LocalStorage(path)
        sr = storage.serializer
        sr.register("identity", IdentityComponentSerializer())
        sr.register("definition", DefinitionComponentSerializer())
        sr.register("links", LinksComponentSerializer(storage))
        return storage
    return __get_storage


@pytest.fixture(name="storage")
def __storage(get_storage):
    return get_storage(None)
