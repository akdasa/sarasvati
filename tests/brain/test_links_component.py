import pytest

from sarasvati.brain import Thought


def test_add():
    t1 = Thought()
    t2 = Thought()
    lk = t1.links.add(t2, "child")
    assert lk.source == t1
    assert lk.destination == t2
    assert lk.kind == "child"


def test_add_twice_raises_error():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    with pytest.raises(Exception):
        t1.links.add(t2, "child")


def test_remove():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    t1.links.remove(t2)
    assert t1.links.count == 0


def test_remove_nonexistent_raises_error():
    t1 = Thought()
    with pytest.raises(Exception):
        t1.links.remove(Thought())


def test_count():
    t1 = Thought()
    assert t1.links.count == 0
    t1.links.add(Thought(), "child")
    assert t1.links.count == 1


def test_children():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    assert t1.links.children[0] == t2


def test_parents():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "parent")
    assert t1.links.parents[0] == t2


def test_references():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "reference")
    assert t1.links.references[0] == t2


def test_incorrect_kind_raises_error():
    t1 = Thought()
    with pytest.raises(ValueError):
        t1.links.add(Thought(), "incorrect")


def test_link_to_itself_raises_error():
    t1 = Thought()
    with pytest.raises(ValueError):
        t1.links.add(t1, "child")


def test_linked_entity_without_storage_specified():
    t1 = Thought()
    with pytest.raises(Exception) as ex:
        t1.links.deserialize([{"key": "test2", "kind": "child"}])
    assert ex.value.args[0] == "No 'get_linked' specified to load linked thoughts"


def test_empty_links_without_storage_specified():
    t1 = Thought()
    t1.links.deserialize([])  # should not raise exception
