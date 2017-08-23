from sarasvati.brain import Thought
from sarasvati.brain.model import Model


def test_serialization_component_is_accessible():
    t = Thought()
    assert t.serialization is not None


def test_serialization():
    t = Thought("Root", "Description")
    r = t.serialization.serialize()
    assert r == {
        "identity": {"key": t.key},
        "definition": {"title": "Root", "description": "Description"}}


def test_serialization_links():
    t = Thought("Root", "Description")
    a = Thought("Another", "Thought")
    t.links.add(a, "child")
    r = t.serialization.serialize()
    assert r == {
        "identity": {"key": t.key},
        "definition": {"title": "Root", "description": "Description"},
        "links": [{"key": a.key, "kind": "child"}]}


def test_deserialization():
    t = Thought()
    t.serialization.deserialize({
        "identity": {"key": "my-id"},
        "definition": {"title": "root", "description": "some text"}})
    assert t.key == "my-id"
    assert t.title == "root"
    assert t.description == "some text"


def test_deserialization_create_component():
    m = Model()
    m.serialization.deserialize({
        "definition": {"title": "component", "description": "should create"}
    })
    assert m.get_component("definition") is not None
    assert m.definition is not None
    assert m.definition.title == "component"
    assert m.definition.description == "should create"


def test_deserialization_component_with_init_params():
    m = Model()
    m.serialization.deserialize({
        "links": {}
    })
    assert m.links is not None
