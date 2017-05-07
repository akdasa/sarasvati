from api.brain.model import Component


def test_init_component():
    c = Component("My")
    assert c.name == "My"
