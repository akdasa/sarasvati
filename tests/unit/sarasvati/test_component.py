from sarasvati.models import Component


def test_component_init():
    """Init component with name"""
    c = MyComponent("My")
    assert c.name == "My"

# Tests configuration


class MyComponent(Component):
    def __init__(self, name):
        super().__init__(name)
