import pytest

from sarasvati.brain.model import Composite, Component


def test_composite_has_no_components_after_init():
    ct = Composite()
    assert len(ct.components) == 0


def test_composite_init_with_specified_components():
    c = Component(name="test")
    ct = Composite(components=[c])
    assert len(ct.components) == 1


def test_composite_unable_to_init_with_same_components():
    c1 = Component(name="test")
    c2 = Component(name="test")
    with pytest.raises(Exception):
        Composite(components=[c1, c2])


def test_composite_add_component():
    c = Component(name="test")
    ct = Composite()
    ct.add_component(c)
    assert len(ct.components) == 1


def test_composite_add_components():
    c1 = Component(name="test1")
    c2 = Component(name="test2")
    ct = Composite()
    ct.add_components([c1, c2])
    assert len(ct.components) == 2
    assert ct.has_component("test1")
    assert ct.has_component("test2")


def test_composite_add_component_twice():
    c = Component(name="test")
    ct = Composite()
    with pytest.raises(Exception):
        ct.add_component(c)
        ct.add_component(c)


def test_component_add_component_already_been_added_at_init():
    c = Component(name="test")
    ct = Composite(components=[c])
    with pytest.raises(Exception):
        ct.add_component(c)


def test_composite_has_component():
    c = Component(name="test")
    ct = Composite(components=[c])
    assert ct.has_component("test") is True
    assert ct.has_component("another") is False


def test_composite_get_component():
    c = Component(name="test")
    ct = Composite(components=[c])
    assert c == ct.get_component("test")


def test_composite_get_non_existent_component():
    ct = Composite()
    with pytest.raises(Exception):
        ct.get_component("no")


def test_composite_access_to_component_by_property():
    c = Component(name="test")
    ct = Composite(components=[c])
    assert ct.test is not None


def test_composite_access_to_non_existent_component_by_property():
    ct = Composite()
    with pytest.raises(Exception) as ex:
        ct.non_existent_component.do()
    assert ex.value.args[0] == "Component 'non_existent_component' not found for '" + str(ct) + "'"


def test_component_list_of_components():
    c1 = Component(name="test1")
    c2 = Component(name="test2")
    ct = Composite()
    ct.add_components([c1, c2])
    assert sorted(list(ct.components), key=lambda x: x.name) == [c1, c2]
