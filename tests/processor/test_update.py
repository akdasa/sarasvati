import pytest

from sarasvati.commands import CommandException


def test_update(api):
    thought = api.processor.execute("/c new").value
    updated = api.processor.execute("/u new title:TITLE desc:DESC").value

    assert thought == updated
    assert thought.title == "TITLE"
    assert thought.description == "DESC"


def test_update_activated(api):
    thought = api.processor.execute("/c new").value
    api.processor.execute("/a new")
    api.processor.execute("/u title:TITLE_NEW desc:DESC_NEW")

    assert thought.title == "TITLE_NEW"
    assert thought.description == "DESC_NEW"


def test_update_nothing(api):
    api.processor.execute("/c new")
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/u new")
    assert exc.value.args[0] == "Nothing to do"


def test_update_not_found(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/u new title:old")
    assert exc.value.args[0] == "No 'new' thought found"

def test_update_no_active(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/u title:old")
    assert exc.value.args[0] == "No title specified nor activated thought"
