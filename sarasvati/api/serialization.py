from sarasvati.brain.model import IdentityComponent, IdentityComponentSerializer
from sarasvati.models import Component
from sarasvati.brain.thought import DefinitionComponent, LinksComponent, Thought, DefinitionComponentSerializer, \
    LinksComponentSerializer


class SarasvatiSerializationApiComponent(Component):
    COMPONENT_NAME = "serialization"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__options = {}
        self.__api = None
        self.register(IdentityComponent.COMPONENT_NAME, IdentityComponent)
        self.register(DefinitionComponent.COMPONENT_NAME, DefinitionComponent)
        self.register(LinksComponent.COMPONENT_NAME, LinksComponent)

    def register(self, component_name, component_class):
        self.__options[component_name] = component_class

    def get(self, name):
        storage = self.__api.storage
        return {
            IdentityComponent.COMPONENT_NAME: IdentityComponentSerializer(),
            DefinitionComponent.COMPONENT_NAME: DefinitionComponentSerializer(),
            LinksComponent.COMPONENT_NAME: LinksComponentSerializer(self.__get_linked(storage))
        }.get(name, None)

    @staticmethod
    def __get_linked(storage):
        def result(key):
            cached = storage.cache.get(key)
            if not cached:
                thought = Thought("<LAZY>", key=key)
                storage.cache.add(thought, lazy=True)
                return thought
            else:
                return cached
        return result

    def on_added(self, composite):
        self.__api = composite
