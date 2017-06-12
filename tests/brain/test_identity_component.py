import pytest

from sarasvati.brain.model import IdentityComponent


def test_identity_component_init():
    i = IdentityComponent()
    assert i.key is not None


def test_identity_component_generates_unique_id():
    i1 = IdentityComponent()
    i2 = IdentityComponent()
    assert i1.key != i2.key


def test_identity_component_init_with_key():
    i = IdentityComponent(key="my_key")
    assert i.key is "my_key"


def test_identity_component_key_set():
    i = IdentityComponent()
    i.key = "my_key"
    assert i.key is "my_key"


def test_identity_component_deserialize_without_key():
    i = IdentityComponent()
    with pytest.raises(Exception):
        i.deserialize({"test": "123"})


def test_identity_component_serialize():
    i = IdentityComponent()
    assert i.serialize() == {"key": i.key}


def test_identity_component_deserialize():
    i = IdentityComponent()
    i.deserialize({"key": "123"})
    assert i.key == "123"
