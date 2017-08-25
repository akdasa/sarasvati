import pytest

from plugins.storage.local import LocalStorage
from sarasvati.brain import Thought


@pytest.fixture
def storage_one(storage):
    root = Thought("Root", key="root")
    child1 = Thought("Child", key="child")
    child2 = Thought("Child2", key="child2")

    root.links.add(child1, "child")
    child1.links.add(root, "parent")

    child1.links.add(child2, "child")
    child2.links.add(child1, "parent")

    storage.add(root)
    storage.add(child1)
    storage.add(child2)
    storage.cache.clear()
    return storage
