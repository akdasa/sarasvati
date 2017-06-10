from sarasvati import get_api


class SarasvatiApplication:
    def __init__(self):
        self._api = get_api()
        self._brain = self._api.open_brain(".")
        self._processor = self._api.plugins.get("processor").get()
