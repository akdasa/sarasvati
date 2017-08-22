from plugins.app.gui.plex import PlexStateDiffLine
from sarasvati.brain import Thought


def test_init():
    t1 = Thought()
    state1 = PlexStateDiffLine(t1, "root", "child")
    assert state1.thought == t1
    assert state1.old_state == "root"
    assert state1.new_state == "child"


def test_eq():
    t1 = Thought()
    state1 = PlexStateDiffLine(t1, "root", "child")
    state2 = PlexStateDiffLine(t1, "root", "child")
    assert state1 == state2


def test_not_eq():
    t1 = Thought()
    t2 = Thought()
    state1 = PlexStateDiffLine(t1, "root", "child")
    state2 = PlexStateDiffLine(t2, "root", "child")
    assert state1 != state2
