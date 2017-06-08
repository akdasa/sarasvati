import pytest

from sarasvati.brain import Thought


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
    empty_storage.cache.clear()  # clean cache to load from DB not cache
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


def test_load_linked_child_and_parent(storage):
    brain = storage.get("Brain")
    tasks = list(filter(lambda x: x.title == "Tasks", brain.links.children))[0]
    tasks_db = storage.get("Tasks")

    assert tasks is tasks_db
    assert tasks in brain.links.children
    assert brain in tasks.links.parents


def test_load_linked_child_parent_and_lazy_child(storage):
    brain = storage.get("Brain")
    cook = storage.get("Cook cake")
    tasks = storage.get("Tasks")

    assert tasks in brain.links.children
    assert cook in tasks.links.children
    assert brain in tasks.links.parents
    assert tasks in cook.links.parents


def test_cache_linked(storage):
    storage.get("Brain")
    assert storage.cache.is_cached("Brain") is True
    assert storage.cache.is_cached("Tasks") is True
    assert storage.cache.is_cached("Recipes") is True


def test_cache_linked_lazy(storage):
    storage.get("Brain")
    assert storage.cache.is_lazy("Brain") is False
    assert storage.cache.is_lazy("Tasks") is False
    assert storage.cache.is_lazy("Recipes") is False
