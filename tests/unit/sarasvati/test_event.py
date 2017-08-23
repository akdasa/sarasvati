import pytest

from sarasvati.event import Event


def test_event_notify(handler):
    e = Event()
    e.subscribe(handler.func)
    e.notify("data")
    assert handler.handled is True
    assert handler.args == "data"


def test_unable_to_subscribe_same_handler_twice(handler):
    e = Event()
    e.subscribe(handler.func)
    with pytest.raises(Exception):
        e.subscribe(handler.func)


def test_unsubscribe(handler):
    e = Event()
    e.subscribe(handler.func)
    e.unsubscribe(handler.func)
    e.notify("123")
    assert handler.handled is False


def test_unable_to_unsubscribe_not_subscribed(handler):
    e = Event()
    with pytest.raises(Exception):
        e.unsubscribe(handler.func)


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
