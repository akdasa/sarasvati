import pytest

from sarasvati.commands import CommandException


def test_activate(api):
    thought = api.execute("/c new").value
    rt = api.execute("/a new").value
    assert api.brain.state.active_thought == thought
    assert api.brain.state.active_thought == rt


def test_activate_title_arg(api):
    thought = api.execute("/c new").value
    api.execute("/a title:new")
    assert api.brain.state.active_thought == thought


def test_activate_no_title(api):
    api.execute("/c new")
    with pytest.raises(CommandException) as exc:
        api.execute("/a")
    assert exc.value.args[0] == "No title specified"
