import pytest

from plugins.app.gui.application import SarasvatiGuiApplication


@pytest.fixture
def app(empty_brain_path):
    return SarasvatiGuiApplication(brain_path=empty_brain_path)


@pytest.fixture
def empty_brain_path():
    import tempfile
    with tempfile.NamedTemporaryFile(dir='/tmp', delete=False) as file:
        return file.name
