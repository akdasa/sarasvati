import pytest

from plugins.storage import LocalStorage
from sarasvati.api import SarasvatiApi
from sarasvati.brain import Brain


class TestsSarasvatiApi(SarasvatiApi):
    def __init__(self):
        super().__init__()
        self.storage = None
        self.open_brain(None)

    def open_brain(self, path):
        self.storage = LocalStorage(path)
        self.brain = Brain(self.storage)
        return self.brain

_d = TestsSarasvatiApi()


@pytest.fixture
def api():
    return TestsSarasvatiApi()
