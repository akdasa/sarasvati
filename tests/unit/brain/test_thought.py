from sarasvati.brain import Thought


def test_thought_init():
    t = Thought()
    assert t.title is None
    assert t.description is None
    assert t.definition is not None
    assert t.links is not None


def test_init_with_key():
    t = Thought(key="MyKey")
    assert t.key == "MyKey"


def test_init_with_title_and_description():
    t = Thought(title="title", description="desc")
    assert t.title == "title"
    assert t.description == "desc"


def test_set_title():
    t = Thought()
    t.title = "title"
    assert t.title is "title"


def test_set_description():
    t = Thought()
    t.description = "desc"
    assert t.description is "desc"


def test_thought_has_generated_key():
    t = Thought()
    assert t.key is not None


def test_thought_string_representation():
    t = Thought(title="title")
    assert str(t) == "<Thought:" + t.key + "/" + t.title + ">"

