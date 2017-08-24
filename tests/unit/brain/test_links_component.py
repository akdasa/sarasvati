import pytest

from sarasvati.brain import Thought, Link
from sarasvati.exceptions import SarasvatiException
from sarasvati.serialization import LinksComponentSerializer


def test_add():
    t1 = Thought()
    t2 = Thought()
    lk = t1.links.add(t2, "child")
    assert lk.source == t1
    assert lk.destination == t2
    assert lk.kind == "child"


def test_add_twice():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    with pytest.raises(SarasvatiException) as ex:
        t1.links.add(t2, "child")
    assert ex.value.message == "Link to specified thought already exist"


def test_add_self():
    t1 = Thought()
    with pytest.raises(SarasvatiException) as ex:
        t1.links.add(t1, "child")
    assert ex.value.message == "Unable link thought to itself"


def test_remove():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    t1.links.remove(t2)
    assert t1.links.count == 0


def test_remove_not_exist():
    t1 = Thought()
    with pytest.raises(SarasvatiException) as ex:
        t1.links.remove(Thought())
    assert ex.value.message == "Link to specified thought does not exist"


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


def test_incorrect_kind():
    t1 = Thought()
    with pytest.raises(SarasvatiException) as ex:
        t1.links.add(Thought(), "incorrect")
    assert ex.value.message == "Link kind is not correct: incorrect"


def test_linked_entity_without_storage_specified():
    t1 = Thought()
    sr = LinksComponentSerializer()
    with pytest.raises(SarasvatiException) as ex:
        sr.deserialize([{"key": "test2", "kind": "child"}], t1.links)
    assert ex.value.message == "No 'storage' specified to load linked thoughts from"


def test_empty_links_without_storage_specified():
    t1 = Thought()
    sr = LinksComponentSerializer()
    sr.deserialize([], t1.links)  # should not raise exception


def test_add_link():
    t1 = Thought()
    t2 = Thought()
    l1 = Link(source=t1, destination=t2, kind="child")
    l2 = Link(source=t2, destination=t1, kind="parent")
    t1.links.add_link(l1)
    t2.links.add_link(l2)

    assert t2 in t1.links.children
    assert t1 in t2.links.parents


def test_add_link_wrong():
    t1 = Thought()
    t2 = Thought()
    l1 = Link(source=t2, destination=t1, kind="child")
    with pytest.raises(SarasvatiException) as ex:
        t1.links.add_link(l1)
    assert ex.value.message == "link.source points to another thought"
