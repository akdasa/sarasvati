from sarasvati.models import Composite, Component, ComponentSerializer


class MyComposite(Composite):
    def __init__(self, components=None):
        super().__init__(components)


class MyComponent(Component):
    def __init__(self, name, data=None):
        super().__init__(name)
        self.data = data


class MySerializer(ComponentSerializer):
    def serialize(self, component):
        return {"data": component.data}

    def deserialize(self, data, component=None):
        result = component or MyComponent("test")
        result.data = data["data"]
        return result
