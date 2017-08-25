from abc import ABCMeta

from sarasvati import get_api


class SarasvatiApplication(metaclass=ABCMeta):
    def __init__(self):
        self._api = get_api()
