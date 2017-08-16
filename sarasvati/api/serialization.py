from sarasvati.brain.model import IdentityComponent
from sarasvati.models import Component
from sarasvati.brain.thought import DefinitionComponent, LinksComponent, Thought


class SarasvatiSerializationApiComponent(Component):
    COMPONENT_NAME = "serialization"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__options = {}
        self.register(IdentityComponent.COMPONENT_NAME, IdentityComponent)
        self.register(DefinitionComponent.COMPONENT_NAME, DefinitionComponent)
        self.register(LinksComponent.COMPONENT_NAME, LinksComponent)

    def register(self, component_name, component_class):
        self.__options[component_name] = component_class

    def get_options(self, storage):
        return {
            "get_component": self.__get_component,
            "get_linked": self.__get_linked(storage)}

    def __get_component(self, key):
        res = self.__options.get(key, None)
        if res:
            return res()
        return None

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
