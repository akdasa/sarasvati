import pytest

from sarasvati.exceptions import SarasvatiException
from sarasvati.models import Composite, Component, ComponentSerializer
from sarasvati.serializer import Serializer


def test_init():
    """Initialize serializer"""
    assert Serializer() is not None


def test_serialize():
    """Serializes"""
    s = Serializer()
    s.register("test", MySerializer())

    ct = MyComponent("test", "test-data")
    cc = MyComposite(components=[ct])
    rs = s.serialize(cc)
    assert rs == {"test": {"data": "test-data"}}


def test_serializer_not_found():
    """Serializes"""
    s = Serializer()
    ct = MyComponent("test", "test-data")
    cc = MyComposite(components=[ct])
    with pytest.raises(SarasvatiException) as ex:
        s.serialize(cc)
    assert ex.value.message == "No serializer found for 'test'"


def test_deserialize():
    s = Serializer()
    s.register("test", MySerializer())

    dt = {"test": {"data": "test-data"}}
    cc = MyComposite()
    rs = s.deserialize(cc, dt)

    assert rs.has_component("test")
    assert rs.test.data == "test-data"


def test_deserialize_with_component():
    s = Serializer()
    s.register("test", MySerializer())

    dt = {"test": {"data": "test-data"}}
    ct = MyComponent("test", None)
    cc = MyComposite(components=[ct])
    rs = s.deserialize(cc, dt)

    assert rs.has_component("test")
    assert rs.test.data == "test-data"


def test_deserializer_not_found():
    s = Serializer()
    ct = MyComponent("test", "test-data")
    cc = MyComposite(components=[ct])
    dt = {"test": {"data": "test-data"}}
    with pytest.raises(SarasvatiException) as ex:
        s.deserialize(cc, dt)
    assert ex.value.message == "No serializer found for 'test'"

# Tests configuration


class MyComposite(Composite):
    def __init__(self, components=None):
        super().__init__(components)


class MyComponent(Component):
    def __init__(self, name, data=None):
        super().__init__(name)
        self.data = data


class MySerializer(ComponentSerializer):
    def serialize(self, component):
        return {"data": component.data}

    def deserialize(self, data, component=None):
        result = component or MyComponent("test")
        result.data = data["data"]
        return result
