import pytest

from api.models import IdentityComponent


def test_init_with_key_generated():
    i = IdentityComponent()
    assert i.key is not None


def test_generates_unique_id():
    i1 = IdentityComponent()
    i2 = IdentityComponent()
    assert i1.key != i2.key


def test_init_by_specified_key():
    i = IdentityComponent(key="my_key")
    assert i.key is "my_key"


def test_key_set():
    i = IdentityComponent()
    i.key = "my_key"
    assert i.key is "my_key"


def test_deserialize_entity_without_key():
    i = IdentityComponent()
    with pytest.raises(Exception):
        i.deserialize({"test": "123"})
