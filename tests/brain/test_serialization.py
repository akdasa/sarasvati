from api.brain import Thought
from api.brain.model import Model


def test_serialization_component_is_accessible():
    t = Thought()
    assert t.serialization is not None


def test_serialize():
    t = Thought("Root", "Description")
    r = t.serialization.serialize()
    assert r == {
        "identity": {"key": t.key},
        "definition": {"title": "Root", "description": "Description"}}


def test_serialize_links():
    t = Thought("Root", "Description")
    a = Thought("Another", "Thought")
    t.links.add(a, "child")
    r = t.serialization.serialize()
    assert r == {
        "identity": {"key": t.key},
        "definition": {"title": "Root", "description": "Description"},
        "links": [{"key": a.key, "kind": "child"}]}


def test_deserialize(serialization_options):
    t = Thought()
    t.serialization.deserialize({
        "identity": {"key": "my-id"},
        "definition": {"title": "root", "description": "some text"}},
        serialization_options)
    assert t.key == "my-id"
    assert t.title == "root"
    assert t.description == "some text"


def test_deserialize_create_component(serialization_options):
    m = Model()
    m.serialization.deserialize({
        "definition": {"title": "component", "description": "should create"}
    }, serialization_options)
    assert m.get_component("definition") is not None
    assert m.definition is not None
    assert m.definition.title == "component"
    assert m.definition.description == "should create"


def test_deserialize_component_with_init_params(serialization_options):
    m = Model()
    m.serialization.deserialize({
        "links": {}
    }, serialization_options)
    assert m.links is not None
