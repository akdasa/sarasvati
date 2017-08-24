import pytest

from sarasvati.event import Event
from sarasvati.exceptions import SarasvatiException


def test_notify(handler):
    """Notify should call handler function"""
    e = Event()
    e.subscribe(handler.func)
    e.notify("data")
    assert handler.handled is True
    assert handler.args == "data"


def test_subscribe_twice(handler):
    """Second subscription on same handler should raise SarasvatiException"""
    e = Event()
    e.subscribe(handler.func)
    with pytest.raises(SarasvatiException) as ex:
        e.subscribe(handler.func)
    assert ex.value.message == "Already subscribed on specified handler"


def test_unsubscribe(handler):
    """Handler should not be called after unsubscribe"""
    e = Event()
    e.subscribe(handler.func)
    e.unsubscribe(handler.func)
    e.notify("123")
    assert handler.handled is False


def test_unsubscribe_empty(handler):
    """Unsubscribe handler what not been subscribed should raise SarasvatiException"""
    e = Event()
    with pytest.raises(SarasvatiException) as ex:
        e.unsubscribe(handler.func)
    assert ex.value.message == "Not subscribed on specified handler"


# Tests configurations

@pytest.fixture(name="handler")
def __handler():
    class Handler:
        def __init__(self):
            self.args = None
            self.handled = False

        def func(self, args):
            self.args = args
            self.handled = True

    return Handler()
