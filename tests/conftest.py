import pytest

from plugins.storage_local import LocalStorage
from sarasvati.api import SarasvatiApi
from sarasvati.brain import Brain


class TestsSarasvatiApi(SarasvatiApi):
    def __init__(self):
        super().__init__()
        self.open_brain(None)

    def open_brain(self, path):
        storage = LocalStorage(path)
        self.brain = Brain(storage)
        self.execute = self.brain.commands.execute
        return self.brain


@pytest.fixture
def api():
    return TestsSarasvatiApi()
