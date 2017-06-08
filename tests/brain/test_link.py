import pytest

from sarasvati.brain import Thought, Link


def test_invalid_kind():
    with pytest.raises(Exception) as ex:
        t1 = Thought()
        t2 = Thought()
        Link(t1, t2, "invalid")
    assert ex.value.args[0] == "Invalid link kind: invalid"
