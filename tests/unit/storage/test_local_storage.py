import pytest

from sarasvati.brain import Thought
from sarasvati.exceptions import SarasvatiException


def test_get_return_none_with_empty_database(storage):
    assert storage.get("nothing") is None


def test_count_returns_count_of_records(storage, thought):
    storage.add(thought)
    assert storage.count() == 1
    storage.remove(thought)
    assert storage.count() == 0


def test_add_twice_raises_exception(storage, thought):
    storage.add(thought)
    with pytest.raises(Exception):
        storage.add(thought)


def test_get_returns_same_entity(storage, thought):
    storage.add(thought)
    assert storage.get(thought.key) is thought


def test_get_returns_new_entity_after_cache_clean(storage, thought):
    storage.add(thought)
    storage.cache.clear()
    new_thought = storage.get(thought.key)
    assert new_thought is not thought


def test_update_returns_same_entity(storage, thought):
    storage.add(thought)
    storage.update(thought)
    assert storage.get(thought.key) is thought


def test_update_entity(storage, thought):
    storage.add(thought)
    thought.title = "new"
    storage.update(thought)
    storage.cache.clear()  # clean cache to load from DB, not cache
    assert storage.get(thought.key).title == "new"


def test_remove_entity(storage, thought):
    storage.add(thought)
    storage.remove(thought)
    assert storage.get(thought.key) is None


def test_remove_with_links(storage, thought):
    child = Thought(key="Child")
    thought.links.add(child, "child")
    child.links.add(thought, "parent")
    storage.add(thought)
    storage.add(child)
    storage.remove(child)
    storage.cache.clear()
    assert storage.get(thought.key).links.count == 0


def test_remove_entity_twice(storage, thought):
    storage.add(thought)
    storage.remove(thought)
    with pytest.raises(SarasvatiException) as exc:
        storage.remove(thought)
    assert exc.value.message == "Unable to remove a non-existent thought"


def test_load_linked_child(storage, thought):
    child_thought = Thought("Child")
    thought.links.add(child_thought, "child")
    storage.add(thought)
    storage.add(child_thought)
    storage.cache.clear()
    assert storage.get("Root").links.children[0].title == "Child"


# def test_load_linked_child_and_parent(storage):
#     brain = storage.get("Brain")
#     tasks = list(filter(lambda x: x.title == "Tasks", brain.links.children))[0]
#     tasks_db = storage.get("Tasks")
#
#     assert tasks is tasks_db
#     assert tasks in brain.links.children
#     assert brain in tasks.links.parents
#
#
# def test_load_linked_child_parent_and_lazy_child(storage):
#     brain = storage.get("Brain")
#     cook = storage.get("Task2")
#     tasks = storage.get("Tasks")
#
#     assert tasks in brain.links.children
#     assert cook in tasks.links.children
#     assert brain in tasks.links.parents
#     assert tasks in cook.links.parents
#
#
# def test_cache_linked(storage):
#     storage.get("Brain")
#     assert storage.cache.is_cached("Brain") is True
#     assert storage.cache.is_cached("Tasks") is True
#     assert storage.cache.is_cached("Recipes") is True
#
#
# def test_cache_linked_nearest_not_lazy(storage):
#     storage.get("Brain")
#     assert storage.cache.is_lazy("Brain") is False
#     assert storage.cache.is_lazy("Tasks") is False
#     assert storage.cache.is_lazy("Recipes") is False
#
#
# def test_cache_linked_far_lazy(storage):
#     storage.get("Brain")
#     assert storage.cache.is_lazy("Task1") is True
