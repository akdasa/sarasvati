import pytest

from sarasvati.exceptions import CommandException


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
    assert exc.value.args[0] == "No title or key specified"


def test_activate_title_and_key(api):
    api.execute("/c New Thought key:new")
    with pytest.raises(CommandException) as exc:
        api.execute("/a New Thought key:new")
    assert exc.value.args[0] == "The name and key can not be used at the same time"


def test_activate_key(api):
    api.execute("/c New Thought key:new")
    found = api.execute("/a key:new").value
    assert found.title == "New Thought"
