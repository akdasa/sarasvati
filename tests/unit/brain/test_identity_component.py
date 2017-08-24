import pytest

from sarasvati.brain.model import IdentityComponent
from sarasvati.exceptions import SarasvatiException
from sarasvati.serialization import IdentityComponentSerializer


def test_init():
    i = IdentityComponent()
    assert i.key is not None


def test_unique_id():
    i1 = IdentityComponent()
    i2 = IdentityComponent()
    assert i1.key != i2.key


def test_init_with_key():
    i = IdentityComponent(key="my_key")
    assert i.key is "my_key"


def test_key_set():
    i = IdentityComponent()
    i.key = "my_key"
    assert i.key is "my_key"


def test_deserialize_without_key():
    i = IdentityComponent()
    s = IdentityComponentSerializer()
    with pytest.raises(SarasvatiException) as ex:
        s.deserialize({"test": "123"}, i)
    assert ex.value.message == "Required 'key' does not present in data"


def test_serialize():
    i = IdentityComponent()
    s = IdentityComponentSerializer()
    assert s.serialize(i) == {"key": i.key}


def test_deserialize():
    i = IdentityComponent()
    s = IdentityComponentSerializer()
    s.deserialize({"key": "123"}, i)
    assert i.key == "123"
