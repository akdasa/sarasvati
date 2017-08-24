from sarasvati.brain.model import IdentityComponent
from sarasvati.brain.thought import DefinitionComponent, LinksComponent, Thought
from sarasvati.models import ComponentSerializer


class IdentityComponentSerializer(ComponentSerializer):
    def serialize(self, component):
        return {"key": component.key}

    def deserialize(self, data, component=None):
        result = component or IdentityComponent()
        if "key" not in data:
            raise Exception("Required 'key' does not present in data")
        result.key = data.get("key", None)
        return result


class DefinitionComponentSerializer(ComponentSerializer):
    def serialize(self, component=None):
        return {"title": component.title,
                "description": component.description}

    def deserialize(self, data, component=None):
        result = component or DefinitionComponent()
        result.title = data.get("title", None)
        result.description = data.get("description", None)
        return result


class LinksComponentSerializer(ComponentSerializer):
    def __init__(self, storage=None):
        self.__storage = storage

    def serialize(self, component):
        result = []
        for key in component.all:
            l = component.all[key]
            result.append({"key": l.destination.key, "kind": l.kind})
        if len(result) == 0:
            return None
        return result

    def deserialize(self, data, component=None, options=None):
        result = component or LinksComponent()
        links_count = len(data)

        # get storage to retrieve linked thoughts
        if self.__storage is None and links_count > 0:
            raise Exception("No 'storage' specified to load linked thoughts from")

        for link in data:  # create lazy Thoughts for each link
            thought = self.__get_linked(link["key"])
            result.add(thought, link["kind"])

        return result

    def __get_linked(self, key):
        cached = self.__storage.cache.get(key)
        if not cached:
            thought = Thought("<LAZY>", key=key)
            self.__storage.cache.add(thought, lazy=True)
            return thought
        else:
            return cached
