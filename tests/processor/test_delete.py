import pytest

from sarasvati.commands import CommandException


def test_delete(api):
    created = api.processor.execute("/c new").value
    deleted = api.processor.execute("/d new").value

    result = api.brain.search.by_title("new")
    assert len(result) == 0
    assert created == deleted


def test_delete_activated(api):
    api.processor.execute("/c new")
    api.processor.execute("/a new")
    api.processor.execute("/d")

    result = api.brain.search.by_title("new")
    assert len(result) == 0


def test_delete_no_title_specified(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/d")
    assert exc.value.args[0] == "No title specified nor activated thought"
