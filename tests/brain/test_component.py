from sarasvati.models import Component


def test_component_smoke():
    c = Component("my")
    c.serialize()
    c.deserialize({})


def test_component_init():
    c = Component("My")
    assert c.name == "My"
