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


@pytest.fixture
def script(app):
    def __script(lines):
        for line in lines:
            app.api.execute(line)
    return __script
