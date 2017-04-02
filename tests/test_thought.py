from api.models import Thought

TITLE = "My Thought"
DESCRIPTION = "Some Description"


def test_init_with_default_values():
    t = Thought()
    assert t.title is None
    assert t.description is None


def test_init_with_title_and_description():
    t = Thought(title=TITLE, description=DESCRIPTION)
    assert t.title == TITLE
    assert t.description == DESCRIPTION


def test_set_title():
    t = Thought()
    t.title = TITLE
    assert t.title is TITLE


def test_set_description():
    t = Thought()
    t.description = DESCRIPTION
    assert t.description is DESCRIPTION


def test_definition_component_is_accessible():
    t = Thought()
    assert t.definition is not None


def test_links_component_is_accessible():
    t = Thought()
    assert t.links is not None


def test_thought_has_generated_key():
    t = Thought()
    assert t.key is not None


def test_thought_string_representation():
    t = Thought(title=TITLE)
    assert str(t) == "<Thought:" + t.key + "/" + t.title + ">"
