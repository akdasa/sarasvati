import pytest

from sarasvati.brain import Thought, Link


def test_links_component_add():
    t1 = Thought()
    t2 = Thought()
    lk = t1.links.add(t2, "child")
    assert lk.source == t1
    assert lk.destination == t2
    assert lk.kind == "child"


def test_links_component_add_twice():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    with pytest.raises(Exception):
        t1.links.add(t2, "child")


def test_links_component_remove():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    t1.links.remove(t2)
    assert t1.links.count == 0


def test_links_component_remove_non_existent():
    t1 = Thought()
    with pytest.raises(Exception):
        t1.links.remove(Thought())


def test_links_component_count():
    t1 = Thought()
    assert t1.links.count == 0
    t1.links.add(Thought(), "child")
    assert t1.links.count == 1


def test_links_component_children():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "child")
    assert t1.links.children[0] == t2


def test_parents():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "parent")
    assert t1.links.parents[0] == t2


def test_links_component_references():
    t1 = Thought()
    t2 = Thought()
    t1.links.add(t2, "reference")
    assert t1.links.references[0] == t2


def test_links_component_incorrect_kind():
    t1 = Thought()
    with pytest.raises(ValueError):
        t1.links.add(Thought(), "incorrect")


def test_links_component_link_to_itself():
    t1 = Thought()
    with pytest.raises(ValueError):
        t1.links.add(t1, "child")


def test_links_component_linked_entity_without_storage_specified():
    t1 = Thought()
    with pytest.raises(Exception) as ex:
        t1.links.deserialize([{"key": "test2", "kind": "child"}])
    assert ex.value.args[0] == "No 'get_linked' specified to load linked thoughts"


def test_links_component_empty_links_without_storage_specified():
    t1 = Thought()
    t1.links.deserialize([])  # should not raise exception


def test_links_component_add_link():
    t1 = Thought()
    t2 = Thought()
    l1 = Link(source=t1, destination=t2, kind="child")
    l2 = Link(source=t2, destination=t1, kind="parent")
    t1.links.add_link(l1)
    t2.links.add_link(l2)

    assert t2 in t1.links.children
    assert t1 in t2.links.parents


def test_links_component_add_wrong_link():
    t1 = Thought()
    t2 = Thought()
    l1 = Link(source=t2, destination=t1, kind="child")
    with pytest.raises(ValueError) as ex:
        t1.links.add_link(l1)
    assert ex.value.args[0] == "link.source: points to another thought"
