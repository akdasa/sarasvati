from sarasvati.brain import Thought
from sarasvati.brain.model import Model


def test_serialization(serializer):
    t = Thought("Root", "Description")
    r = serializer.serialize(t)
    assert r == {
        "identity": {"key": t.key},
        "definition": {"title": "Root", "description": "Description"}}


def test_serialization_links(serializer):
    t = Thought("Root", "Description")
    a = Thought("Another", "Thought")
    t.links.add(a, "child")
    r = serializer.serialize(t)
    assert r == {
        "identity": {"key": t.key},
        "definition": {"title": "Root", "description": "Description"},
        "links": [{"key": a.key, "kind": "child"}]}


def test_deserialization(serializer):
    t = Thought()
    serializer.deserialize(t, {
        "identity": {"key": "my-id"},
        "definition": {"title": "root", "description": "some text"}})
    assert t.key == "my-id"
    assert t.title == "root"
    assert t.description == "some text"


def test_deserialization_create_component(serializer):
    m = Model()
    serializer.deserialize(m, {
        "definition": {"title": "component", "description": "should create"}
    })
    assert m.get_component("definition") is not None
    assert m.definition is not None
    assert m.definition.title == "component"
    assert m.definition.description == "should create"


def test_deserialization_component_with_init_params(serializer):
    m = Model()
    serializer.deserialize(m, {
        "links": {}
    })
    assert m.links is not None
