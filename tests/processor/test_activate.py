import pytest

from sarasvati.commands import CommandException


def test_activate(api):
    thought = api.processor.execute("/c new").value
    rt = api.processor.execute("/a new").value
    assert api.brain.state.active_thought == thought
    assert api.brain.state.active_thought == rt


def test_activate_title_arg(api):
    thought = api.processor.execute("/c new").value
    api.processor.execute("/a title:new")
    assert api.brain.state.active_thought == thought


def test_activate_no_title(api):
    api.processor.execute("/c new")
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/a")
    assert exc.value.args[0] == "No title specified"
