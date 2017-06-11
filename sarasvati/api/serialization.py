from sarasvati.brain.model import IdentityComponent, Component
from sarasvati.brain.thought import DefinitionComponent, LinksComponent, Thought


class SarasvatiSerializationApiComponent(Component):
    COMPONENT_NAME = "serialization"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)

    def get_options(self, storage):
        return {
            "get_component": self.__get_component,
            "get_linked": self.__get_linked(storage)}

    @staticmethod
    # TODO: set serialization map
    def __get_component(key):
        options = {
            IdentityComponent.COMPONENT_NAME: IdentityComponent,
            DefinitionComponent.COMPONENT_NAME: DefinitionComponent,
            LinksComponent.COMPONENT_NAME: LinksComponent}
        res = options.get(key, None)
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