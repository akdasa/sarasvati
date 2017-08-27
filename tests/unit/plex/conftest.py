import pytest

from plugins.app.gui.plex import Plex
from sarasvati.brain import Thought


@pytest.fixture
def plex():
    return Plex()


@pytest.fixture
def thoughts():
    return {
        "Root": Thought("Root"),
        "Child1": Thought("Child1"),
        "Child2": Thought("Child2")
    }
