import pytest

from sarasvati.exceptions import SarasvatiException
from sarasvati.serializer import Serializer


def test_init():
    """Initialize serializer"""
    assert Serializer() is not None


def test_serialize(composite, component, serializer):
    """Serializes"""
    s = Serializer()
    s.register("test", serializer())

    ct = component("test", "test-data")
    cc = composite(components=[ct])
    rs = s.serialize(cc)
    assert rs == {"test": {"data": "test-data"}}


def test_serializer_not_found(composite, component):
    """Serializes"""
    s = Serializer()
    ct = component("test", "test-data")
    cc = composite(components=[ct])
    with pytest.raises(SarasvatiException) as ex:
        s.serialize(cc)
    assert ex.value.message == "No serializer found for 'test'"


def test_deserialize(composite, serializer):
    s = Serializer()
    s.register("test", serializer())

    dt = {"test": {"data": "test-data"}}
    cc = composite()
    rs = s.deserialize(cc, dt)

    assert rs.has_component("test")
    assert rs.test.data == "test-data"


def test_deserialize_with_component(composite, component, serializer):
    s = Serializer()
    s.register("test", serializer())

    dt = {"test": {"data": "test-data"}}
    ct = component("test", None)
    cc = composite(components=[ct])
    rs = s.deserialize(cc, dt)

    assert rs.has_component("test")
    assert rs.test.data == "test-data"


def test_deserializer_not_found(composite, component):
    s = Serializer()
    ct = component("test", "test-data")
    cc = composite(components=[ct])
    dt = {"test": {"data": "test-data"}}
    with pytest.raises(SarasvatiException) as ex:
        s.deserialize(cc, dt)
    assert ex.value.message == "No serializer found for 'test'"
