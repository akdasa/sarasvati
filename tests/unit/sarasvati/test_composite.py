import pytest

from sarasvati.exceptions import SarasvatiException


def test_init_empty(composite):
    """Composite have no components after init"""
    ct = composite()
    assert len(ct.components) == 0


def test_init_with_component(composite, component):
    """Composite have components passed in constructor"""
    cc = component(name="test")
    ct = composite(components=[cc])
    assert len(ct.components) == 1


def test_init_same_components(composite, component):
    """Unable to add component with same name twice"""
    c1 = component(name="test")
    c2 = component(name="test")
    with pytest.raises(SarasvatiException) as ex:
        composite(components=[c1, c2])
    assert ex.value.message == "Component 'test' already exist"


def test_add_component(composite, component):
    """Add component to composite"""
    c = component(name="test")
    ct = composite()
    ct.add_component(c)
    assert len(ct.components) == 1


def test_add_components(composite, component):
    """Add multiple components"""
    c1 = component(name="test1")
    c2 = component(name="test2")
    ct = composite()
    ct.add_components([c1, c2])
    assert len(ct.components) == 2
    assert ct.has_component("test1")
    assert ct.has_component("test2")


def test_add_component_twice(composite, component):
    """Unable to add same component twice"""
    c = component(name="test")
    ct = composite()
    with pytest.raises(SarasvatiException) as ex:
        ct.add_component(c)
        ct.add_component(c)
    assert ex.value.message == "Component 'test' already exist"


def test_add_same_component(composite, component):
    """Unable to add same component again"""
    c = component(name="test")
    ct = composite(components=[c])
    with pytest.raises(SarasvatiException) as ex:
        ct.add_component(c)
    assert ex.value.message == "Component 'test' already exist"


def test_has_component(composite, component):
    """has_component returns true if component exist"""
    c = component(name="test")
    ct = composite(components=[c])
    assert ct.has_component("test") is True
    assert ct.has_component("another") is False


def test_get_component(composite, component):
    """get_component returns component by name"""
    cc = component(name="test")
    ct = composite(components=[cc])
    assert cc == ct.get_component("test")


def test_get_component_doesnt_exist(composite):
    """If you take the component of which does not exist, an exception is thrown."""
    ct = composite()
    with pytest.raises(SarasvatiException) as ex:
        ct.get_component("no")
    assert ex.value.message == "Component 'no' not found for 'MyComposite'"


def test_component_by_property(composite, component):
    """A component can be accessed by property"""
    c = component(name="test")
    ct = composite(components=[c])
    assert ct.test is not None


def test_component_by_property_doesnt_exist(composite):
    """A component can be accessed by property"""
    ct = composite()
    with pytest.raises(SarasvatiException) as ex:
        ct.non_existent_component.do()
    assert ex.value.message == "Component 'non_existent_component' not found for 'MyComposite'"


def test_components_list(composite, component):
    """components property returns list of components"""
    c1 = component(name="test1")
    c2 = component(name="test2")
    ct = composite()
    ct.add_components([c1, c2])
    assert sorted(list(ct.components), key=lambda x: x.name) == [c1, c2]
