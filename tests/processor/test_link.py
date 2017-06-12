import pytest

from sarasvati.commands import CommandException


def test_link(api):
    one = api.processor.execute("/c one").value
    two = api.processor.execute("/c two").value
    api.processor.execute("/l two to:one as:child")

    assert two in one.links.children
    assert one in two.links.parents


def test_link_activated(api):
    one = api.processor.execute("/c one").value
    two = api.processor.execute("/c two").value
    api.processor.execute("/a two")
    api.processor.execute("/l to:one as:child")

    assert two in one.links.children
    assert one in two.links.parents


def test_link_no_title(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l")
    assert exc.value.args[0] == "No title specified nor activated thought"


def test_link_no_to_argument(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l 123")
    assert exc.value.args[0] == "No 'to' argument specified"


def test_link_no_as_argument(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l 123 to:qwe")
    assert exc.value.args[0] == "No 'as' argument specified"


def test_link_wrong_as_argument(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l 123 to:qwe as:wrong")
    assert exc.value.args[0] == "Wrong link type in 'as' argument"


def test_link_thought_not_found(api):
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l child to:parent as:child")
    assert exc.value.args[0] == "No 'child' thought found"


def test_link_to_thought_not_found(api):
    api.processor.execute("/c child")
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l child to:parent as:child")
    assert exc.value.args[0] == "No 'parent' thought found for 'to' argument"


def test_link_not_activated(api):
    api.processor.execute("/c parent")
    with pytest.raises(CommandException) as exc:
        api.processor.execute("/l to:parent as:child")
    assert exc.value.args[0] == "No title specified nor activated thought"
