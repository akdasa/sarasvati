from sarasvati.brain.serialization import IdentityComponentSerializer, DefinitionComponentSerializer, \
    LinksComponentSerializer
from sarasvati.brain.thought import Thought
from sarasvati.models import Component


class SarasvatiSerializationApiComponent(Component):
    COMPONENT_NAME = "serialization"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__options = {}
        self.__api = None
        self.register("identity", IdentityComponentSerializer())
        self.register("definition", DefinitionComponentSerializer())
        self.register("links", LinksComponentSerializer(self.__get_linked))

    def register(self, name, serializer):
        self.__options[name] = serializer

    def get(self, name):
        return self.__options.get(name, None)

    def __get_linked(self, key):
        storage = self.__api.storage
        cached = storage.cache.get(key)
        if not cached:
            thought = Thought("<LAZY>", key=key)
            storage.cache.add(thought, lazy=True)
            return thought
        else:
            return cached

    def on_added(self, composite):
        self.__api = composite
