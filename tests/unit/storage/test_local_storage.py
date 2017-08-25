import pytest

from sarasvati.brain import Thought
from sarasvati.exceptions import SarasvatiException


def test_get_return_none_if_nothing_found(storage):
    """Get returns none if nothing found"""
    assert storage.get("nothing") is None


def test_count_returns_count_of_records(storage, thought):
    """Count returns count of records in storage"""
    storage.add(thought)
    assert storage.count() == 1
    storage.remove(thought)
    assert storage.count() == 0


def test_add_twice_raises_exception(storage):
    """Add raises exception if same thought been added"""
    thought = Thought("Brain", key="root")
    storage.add(thought)
    with pytest.raises(SarasvatiException) as ex:
        storage.add(thought)
    assert ex.value.message == "Thought with same key 'root/Brain' already exist"


def test_get_returns_same_entity(storage, thought):
    """Get returns same entity been added before"""
    storage.add(thought)
    assert storage.get(thought.key) is thought


def test_get_returns_new_entity_if_cache_cleared(storage, thought):
    """Get returns new entity if cache been cleared"""
    storage.add(thought)
    storage.cache.clear()
    assert storage.get(thought.key) is not thought


def test_get_returns_same_entity_after_update(storage, thought):
    """Get returns same entity after update"""
    storage.add(thought)
    storage.update(thought)
    assert storage.get(thought.key) is thought


def test_update_entity(storage):
    """Update entity"""
    thought = Thought("Root")
    storage.add(thought)
    thought.title = "new"
    storage.update(thought)
    storage.cache.clear()  # clean cache to load from DB, not cache
    assert storage.get(thought.key).title == "new"


def test_remove_entity(storage, thought):
    """Remove entity from storage"""
    storage.add(thought)
    storage.remove(thought)
    assert storage.get(thought.key) is None


def test_remove_with_links(storage_one):
    """Remove links to deleting thought"""
    child = storage_one.get("child")
    storage_one.remove(child)
    storage_one.cache.clear()
    assert storage_one.get("root").links.count == 0


def test_remove_entity_twice(storage, thought):
    """Unable to delete thought what doesn't present in storage"""
    storage.add(thought)
    storage.remove(thought)
    with pytest.raises(SarasvatiException) as exc:
        storage.remove(thought)
    assert exc.value.message == "Unable to remove a non-existent thought"


def test_load_linked_child(storage_one):
    """Storage loads linked children too"""
    assert storage_one.get("root").links.children[0].title == "Child"


def test_cache_linked(storage_one):
    """Far thoughts are marked as lazy and not loaded"""
    storage_one.get("root")
    assert storage_one.cache.is_cached("root") is True
    assert storage_one.cache.is_cached("child") is True
    assert storage_one.cache.is_lazy("child") is False


def test_cache_linked_lazy(storage_one):
    """Far thoughts are marked as lazy and not loaded"""
    storage_one.get("root")
    assert storage_one.cache.is_cached("child2") is True
    assert storage_one.cache.is_lazy("child2") is True


def test_cache_root_and_far(storage_one):
    """Root and child2 points to each other through 'child'"""
    root = storage_one.get("root")
    child2 = storage_one.get("child2")

    assert root.links.children[0].links.children[0] == child2
    assert child2.links.parents[0].links.parents[0] == root
    assert storage_one.cache.is_cached("child")
    assert not storage_one.cache.is_lazy("child")


def test_db_same_key(get_storage):
    """Storage raises exception if key is not unique"""
    s = get_storage("tests/unit/storage/assets/db_same_key.json")
    with pytest.raises(SarasvatiException) as ex:
        s.get("123")
    assert ex.value.message == "Entity is not unique 123"


def test_db_error(get_storage):
    """Storage raises exception is error while processing entry occurred"""
    s = get_storage("tests/unit/storage/assets/db_error.json")
    with pytest.raises(SarasvatiException) as ex:
        s.get("123")
    assert ex.value.message == "Error while processing DB entry: No serializer found for 'wrong_component'"


def test_db_link_error(get_storage):
    """Storage raises exception if links points on wrong thought"""
    s = get_storage("tests/unit/storage/assets/db_link_error.json")
    with pytest.raises(SarasvatiException) as ex:
        s.get("123")
    assert ex.value.message == "No link 'wrong_key' found in db"
