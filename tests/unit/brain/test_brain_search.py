import pytest

from sarasvati.brain import Thought


def test_brain_search_by_key(brain):
    t = Thought(key="key")
    brain.storage.add(t)
    r = brain.search.by_key("key")
    assert t is r


def test_brain_search_by_key_returns_none_if_nothing_found(brain):
    r = brain.search.by_key("key")
    assert r is None


def test_brain_search_by_title(full_brain):
    r = full_brain.search.by_title("Thought one")
    assert r is not None
    assert r[0].title == "Thought one"


def test_brain_search_by_title_operator_contains(full_brain):
    r = full_brain.search.by_title("Thought", operator="contains")
    assert r[0].title == "Thought one"
    assert r[1].title == "Thought two"


def test_brain_search_in_description(full_brain):
    r = full_brain.search.in_description("desc")
    assert r[0].title == "Thought one"


# Tests configurations


@pytest.fixture(name="full_brain")
def __full_brain(brain):
    t1 = Thought(title="Thought one", description="desc")
    t2 = Thought(title="Thought two", description="other")
    brain.storage.add(t1)
    brain.storage.add(t2)
    return brain
