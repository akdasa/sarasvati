import pytest

from sarasvati.api import SarasvatiApi


class TestsSarasvatiApi(SarasvatiApi):
    def __init__(self):
        super().__init__()
        self.storage = None
        self.open_brain(None)


_d = TestsSarasvatiApi()


@pytest.fixture
def api():
    return TestsSarasvatiApi()
