import pytest

from plugins.storage.local import LocalStorage
from sarasvati.brain import Brain


@pytest.fixture()
def brain():
    return Brain(LocalStorage(None))
