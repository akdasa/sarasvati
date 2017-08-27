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
        "Child2": Thought("Child2"),
        "Parent1": Thought("Parent1"),
        "Parent2": Thought("Parent2"),
        "Reference1": Thought("Reference1"),
        "Reference2": Thought("Reference2"),
    }
