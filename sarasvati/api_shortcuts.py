from sarasvati import get_api


def get_serializer(name):
    return get_api().serialization.get(name)