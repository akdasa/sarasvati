import pytest

from sarasvati.exceptions import CommandException


def test_delete(api):
    created = api.execute("/c new").value
    deleted = api.execute("/d new").value

    result = api.brain.search.by_title("new")
    assert len(result) == 0
    assert created == deleted


def test_delete_activated(api):
    api.execute("/c new")
    api.execute("/a new")
    api.execute("/d")

    result = api.brain.search.by_title("new")
    assert len(result) == 0


def test_delete_no_title_specified(api):
    with pytest.raises(CommandException) as exc:
        api.execute("/d")
    assert exc.value.args[0] == "No title specified nor activated thought"


def test_delete_not_exist(api):
    with pytest.raises(CommandException) as exc:
        api.execute("/d not_exist")
    assert exc.value.args[0] == "No 'not_exist' thought found"
