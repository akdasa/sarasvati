import pytest

from sarasvati.commands import CommandException


def test_create(api):
    api.execute("/c new thought")

    result = api.brain.search.by_title("new thought")
    assert len(result) == 1
    assert result[0].title == "new thought"


def test_create_by_title(api):
    api.execute("/c title:new thought")

    result = api.brain.search.by_title("new thought")
    assert len(result) == 1
    assert result[0].title == "new thought"


def test_create_and_desc(api):
    api.execute("/c new thought desc:some description")

    result = api.brain.search.by_title("new thought")
    assert result[0].description == "some description"


def test_create_empty_parent(api):
    with pytest.raises(CommandException) as exc:
        api.execute("/c new thought parent:no_parent")
    assert exc.value.args[0] == "No 'no_parent' thought found for 'parent' argument"


def test_create_parent(api):
    api.execute("/c parent")
    api.execute("/c child parent:parent")

    parent = api.brain.search.by_title("parent")[0]
    child = api.brain.search.by_title("child")[0]

    assert child in parent.links.children
    assert parent in child.links.parents


def test_create_as_child(api):
    api.execute("/c parent")
    api.execute("/a parent")
    api.execute("/c child as:child")

    parent = api.brain.search.by_title("parent")[0]
    child = api.brain.search.by_title("child")[0]

    assert child in parent.links.children
    assert parent in child.links.parents


def test_create_as_parent(api):
    api.execute("/c child")
    api.execute("/a child")
    api.execute("/c parent as:parent")

    parent = api.brain.search.by_title("parent")[0]
    child = api.brain.search.by_title("child")[0]

    assert child in parent.links.children
    assert parent in child.links.parents


def test_create_as_reference(api):
    api.execute("/c parent")
    api.execute("/a parent")
    api.execute("/c child as:reference")

    parent = api.brain.search.by_title("parent")[0]
    child = api.brain.search.by_title("child")[0]

    assert child in parent.links.references
    assert parent in child.links.references


def test_create_no_title(api):
    with pytest.raises(CommandException) as exc:
        api.execute("/c")
    assert exc.value.args[0] == "No title specified"


def test_create_parent_and_as(api):
    with pytest.raises(CommandException) as exc:
        api.execute("/c title parent:some as:child")
    assert exc.value.args[0] == "'parent' and 'as' arguments cannot be used simultaneously"


def test_create_as_with_no_active(api):
    with pytest.raises(CommandException) as exc:
        api.execute("/c title as:child")
    assert exc.value.args[0] == "'as' argument can be used only with activated thought"


def test_create_wrong_as(api):
    api.execute("/c title")
    api.execute("/a title")
    with pytest.raises(CommandException) as exc:
        api.execute("/c title as:wrong")
    assert exc.value.args[0] == "Wrong link type in 'as' argument"
