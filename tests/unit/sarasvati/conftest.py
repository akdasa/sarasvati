import pytest

from sarasvati.models import Composite, Component, ComponentSerializer


class MyComposite(Composite):
    def __init__(self, components=None):
        super().__init__(components)


class MyComponent(Component):
    def __init__(self, name, data=None):
        super().__init__(name)
        self.on_added_called = None
        self.data = data

    def on_added(self, composite):
        self.on_added_called = composite


class MySerializer(ComponentSerializer):
    def serialize(self, component):
        return {"data": component.data}

    def deserialize(self, data, component=None):
        result = component or MyComponent("test")
        result.data = data["data"]
        return result


@pytest.fixture(name="composite")
def __composite():
    return MyComposite


@pytest.fixture(name="component")
def __component():
    return MyComponent


@pytest.fixture(name="serializer")
def __serializer():
    return MySerializer
