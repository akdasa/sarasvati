import pytest
from sarasvati.exceptions import SarasvatiException
from sarasvati.models import Composite, Component


def test_init_empty():
    """Composite have no components after init"""
    ct = MyComposite()
    assert len(ct.components) == 0


def test_init_with_component():
    """Composite have components passed in constructor"""
    cc = MyComponent(name="test")
    ct = MyComposite(components=[cc])
    assert len(ct.components) == 1


def test_init_same_components():
    """Unable to add component with same name twice"""
    c1 = MyComponent(name="test")
    c2 = MyComponent(name="test")
    with pytest.raises(SarasvatiException) as ex:
        MyComposite(components=[c1, c2])
    assert ex.value.message == "Component 'test' already exist"


def test_add_component():
    """Add component to composite"""
    c = MyComponent(name="test")
    ct = MyComposite()
    ct.add_component(c)
    assert len(ct.components) == 1


def test_add_components():
    """Add multiple components"""
    c1 = MyComponent(name="test1")
    c2 = MyComponent(name="test2")
    ct = MyComposite()
    ct.add_components([c1, c2])
    assert len(ct.components) == 2
    assert ct.has_component("test1")
    assert ct.has_component("test2")


def test_add_component_twice():
    """Unable to add same component twice"""
    c = MyComponent(name="test")
    ct = MyComposite()
    with pytest.raises(SarasvatiException) as ex:
        ct.add_component(c)
        ct.add_component(c)
    assert ex.value.message == "Component 'test' already exist"


def test_add_same_component():
    """Unable to add same component again"""
    c = MyComponent(name="test")
    ct = MyComposite(components=[c])
    with pytest.raises(SarasvatiException) as ex:
        ct.add_component(c)
    assert ex.value.message == "Component 'test' already exist"


def test_has_component():
    """has_component returns true if component exist"""
    c = MyComponent(name="test")
    ct = MyComposite(components=[c])
    assert ct.has_component("test") is True
    assert ct.has_component("another") is False


def test_get_component():
    """get_component returns component by name"""
    cc = MyComponent(name="test")
    ct = MyComposite(components=[cc])
    assert cc == ct.get_component("test")


def test_get_component_doesnt_exist():
    """If you take the component of which does not exist, an exception is thrown."""
    ct = MyComposite()
    with pytest.raises(SarasvatiException) as ex:
        ct.get_component("no")
    assert ex.value.message == "Component 'no' not found for 'MyComposite'"


def test_component_by_property():
    """A component can be accessed by property"""
    c = MyComponent(name="test")
    ct = MyComposite(components=[c])
    assert ct.test is not None


def test_component_by_property_doesnt_exist():
    """A component can be accessed by property"""
    ct = MyComposite()
    with pytest.raises(SarasvatiException) as ex:
        ct.non_existent_component.do()
    assert ex.value.message == "Component 'non_existent_component' not found for 'MyComposite'"


def test_components_list():
    """components property returns list of components"""
    c1 = MyComponent(name="test1")
    c2 = MyComponent(name="test2")
    ct = MyComposite()
    ct.add_components([c1, c2])
    assert sorted(list(ct.components), key=lambda x: x.name) == [c1, c2]

# Tests configuration


class MyComposite(Composite):
    def __init__(self, components=None):
        super().__init__(components)


class MyComponent(Component):
    def __init__(self, name, data=None):
        super().__init__(name)
        self.data = data
