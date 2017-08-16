from sarasvati.models import Component


def test_component_init():
    c = Component("My")
    assert c.name == "My"
