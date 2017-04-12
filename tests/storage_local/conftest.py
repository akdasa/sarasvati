import pytest

from api.models import Thought
from sarasvati.storage_local import LocalStorage




@pytest.fixture
def empty_storage():
    return LocalStorage(None)


@pytest.fixture
def root_thought():
    t = Thought("Root")
    t.identity.key = "Root"
    return t


@pytest.fixture
def full_storage():
    storage = LocalStorage(None)

    root = Thought("Root")
    child = Thought("Child")
    child2 = Thought("Child2")
    root.links.add(child, "child")
    child.links.add(root, "parent")
    child.links.add(child2, "child")
    child2.links.add(child, "parent")

    root.identity.key = "root"
    child.identity.key = "child"
    child2.identity.key = "child2"

    storage.add(root)
    storage.add(child)
    storage.add(child2)

    storage.cache.thoughts.clear()
    storage.cache.lazy.clear()

    return storage
