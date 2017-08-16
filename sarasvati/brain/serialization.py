from sarasvati.brain.model import IdentityComponent
from sarasvati.brain.thought import DefinitionComponent, LinksComponent
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
    def __init__(self, get_linked=None):
        self.__get_linked = get_linked

    def serialize(self, component):
        result = []
        for key in component.all:
            l = component.all[key]
            result.append({"key": l.destination.key, "kind": l.kind})
        if len(result) == 0:
            return None
        return result

    def deserialize(self, data, component=None):
        result = component or LinksComponent()
        links_count = len(data)

        # get storage to retrieve linked thoughts
        if not self.__get_linked and links_count > 0:
            raise Exception("No 'get_linked' specified to load linked thoughts")

        for link in data:  # create lazy Thoughts for each link
            thought = self.__get_linked(link["key"])
            result.add(thought, link["kind"])

        return result
