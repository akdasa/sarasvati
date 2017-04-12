import pytest
from api.models import Thought
from sarasvati.storage_local import LocalStorage


def test_get_return_none_with_empty_database(empty_storage):
    assert empty_storage.get("nothing") is None


def test_count_returns_count_of_records(empty_storage, root_thought):
    empty_storage.add(root_thought)
    assert empty_storage.count() == 1
    empty_storage.remove(root_thought)
    assert empty_storage.count() == 0


def test_add_twice_raises_exception(empty_storage, root_thought):
    empty_storage.add(root_thought)
    with pytest.raises(Exception):
        empty_storage.add(root_thought)


def test_get_returns_same_entity(empty_storage, root_thought):
    empty_storage.add(root_thought)
    assert empty_storage.get(root_thought.key) is root_thought


def test_get_returns_new_entity_after_cache_clean(empty_storage, root_thought):
    empty_storage.add(root_thought)
    empty_storage.cache.clear()
    new_thought = empty_storage.get(root_thought.key)
    assert new_thought is not root_thought


def test_update_returns_same_entity(empty_storage, root_thought):
    empty_storage.add(root_thought)
    empty_storage.update(root_thought)
    assert empty_storage.get(root_thought.key) is root_thought


def test_update_entity(empty_storage, root_thought):
    empty_storage.add(root_thought)
    root_thought.title = "new"
    empty_storage.update(root_thought)
    assert empty_storage.get(root_thought.key).title == "new"


def test_remove_entity(empty_storage, root_thought):
    empty_storage.add(root_thought)
    empty_storage.remove(root_thought)
    assert empty_storage.get(root_thought.key) is None


def test_load_linked_child(empty_storage, root_thought):
    child_thought = Thought("Child")
    root_thought.links.add(child_thought, "child")
    empty_storage.add(root_thought)
    empty_storage.add(child_thought)
    empty_storage.cache.clear()
    assert empty_storage.get("Root").links.children[0].title == "Child"


def test_load_linked_child_and_parent():
    empty_storage = LocalStorage("./tests/storage_local/fixtures/three_chain.json")

    root = empty_storage.get("Root")
    child = root.links.children[0]
    child_db = empty_storage.get("Child")

    assert child is child_db
    assert root.links.children[0] is child
    assert child.links.parents[0] is root


def test_load_linked_child_parent_and_lazy_child():
    path = "./tests/storage_local/fixtures/three_linked_thoughts.json"
    empty_storage = LocalStorage(path)

    root = empty_storage.get("Root")
    child2 = empty_storage.get("Child_2")
    child = empty_storage.get("Child")

    assert root.links.children[0] is child
    assert child.links.children[0] is child2
    assert child.links.parents[0] is root
    assert child2.links.parents[0] is child


def test_cache_linked(full_storage):
    full_storage.get("root")
    assert full_storage.cache.is_cached("root") is True
    assert full_storage.cache.is_cached("child") is True
    assert full_storage.cache.is_cached("child2") is False


def test_cache_lazy(full_storage):
    full_storage.get("root")
    assert full_storage.cache.is_lazy("root") is False
    assert full_storage.cache.is_lazy("child") is False
    assert full_storage.cache.is_lazy("child2") is True


def test_cache_lazy_child(full_storage):
    full_storage.get("root")
    full_storage.get("child2")
    assert len(full_storage.cache.thoughts) == 3
    assert full_storage.cache.is_lazy("root") is False
    assert full_storage.cache.is_lazy("child") is False
    assert full_storage.cache.is_lazy("child2") is False


def test_cache_lazy_child_near(full_storage):
    full_storage.get("root")
    full_storage.get("child")
    assert full_storage.cache.is_lazy("root") is False
    assert full_storage.cache.is_lazy("child") is False
    assert full_storage.cache.is_lazy("child2") is False


def test_cache_child(full_storage):
    full_storage.get("child")
    assert full_storage.cache.is_lazy("root") is False
    assert full_storage.cache.is_lazy("child") is False
    assert full_storage.cache.is_lazy("child2") is False
