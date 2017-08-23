import pytest

from sarasvati.brain import Thought, Link


def test_link_init():
    t1 = Thought()
    t2 = Thought()
    ln = Link(t1, t2, "child")

    assert ln.source is t1
    assert ln.destination is t2
    assert ln.kind == "child"


def test_link_invalid_kind():
    with pytest.raises(Exception) as ex:
        t1 = Thought()
        t2 = Thought()
        Link(t1, t2, "invalid")
    assert ex.value.args[0] == "Invalid link kind: invalid"
