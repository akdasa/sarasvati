from sarasvati.brain import Thought


def test_search_by_key(brain):
    t = Thought(key="key")
    brain.storage.add(t)
    r = brain.search.by_key("key")
    assert t is r


def test_search_by_key_none(brain):
    r = brain.search.by_key("key")
    assert r is None


def test_search_by_title(full_brain):
    r = full_brain.search.by_title("Thought one")
    assert r is not None
    assert r[0].title == "Thought one"


def test_search_by_title_operator_contains(full_brain):
    r = full_brain.search.by_title("Thought", operator="contains")
    assert r[0].title == "Thought one"
    assert r[1].title == "Thought two"


def test_search_in_description(full_brain):
    r = full_brain.search.in_description("desc")
    assert r[0].title == "Thought one"
