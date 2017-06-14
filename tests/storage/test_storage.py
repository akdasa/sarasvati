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


def test_remove_entity_twice(empty_storage, root_thought):
    empty_storage.add(root_thought)
    empty_storage.remove(root_thought)
    with pytest.raises(Exception) as exc:
        empty_storage.remove(root_thought)
    assert exc.value.args[0] == "Unable to remove a non-existent thought"


def test_remove_entity_links(api):
    api.processor.execute("/c one key:one")
    api.processor.execute("/c two parent:one key:two")
    api.processor.execute("/d one")
    api.storage.cache.clear()

    thought = api.storage.get("two")
    assert len(thought.links.all) == 0
    assert api.storage.get("one") is None


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
    cook = storage.get("Task2")
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


def test_cache_linked_nearest_not_lazy(storage):
    storage.get("Brain")
    assert storage.cache.is_lazy("Brain") is False
    assert storage.cache.is_lazy("Tasks") is False
    assert storage.cache.is_lazy("Recipes") is False


def test_cache_linked_far_lazy(storage):
    storage.get("Brain")
    assert storage.cache.is_lazy("Task1") is True


def test_cache_linked_far_lazy_2(api):
    api.processor.execute("/c root key:root")
    api.processor.execute("/c child1 parent:root key:child1")
    api.processor.execute("/c child2 parent:child1 key:child2")
    api.storage.cache.clear()

    api.processor.execute("/show root")
    api.processor.execute("/show child1")
    assert api.storage.cache.is_lazy("root") is False
    assert api.storage.cache.is_lazy("child1") is False
    assert api.storage.cache.is_lazy("child2") is False


def test_cache_linked_far_lazy_3(api):
    api.processor.execute("/c root key:root")
    api.processor.execute("/c child1 parent:root key:child1")
    api.processor.execute("/c child2 parent:child1 key:child2")
    api.storage.cache.clear()

    api.processor.execute("/show root")
    assert api.storage.cache.is_lazy("child2") is True
