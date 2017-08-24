import pytest

from plugins.app.gui.plex import Plex, PlexLayout, PlexStateDiff
from sarasvati.brain import Brain


@pytest.fixture(name="brain")
def __brain(storage):
    return Brain(storage)


@pytest.fixture(name="plex")
def __plex():
    return Plex()


@pytest.fixture(name="thoughts")
def __thoughts(brain):
    return {
        "Brain": brain.search.by_key("Brain"),
        "Tasks": brain.search.by_key("Tasks"),
        "Recipes": brain.search.by_key("Recipes"),
        "Task1": brain.search.by_key("Task1"),
        "Task2": brain.search.by_key("Task2"),
        "Recipe1": brain.search.by_key("Recipe1"),
        "Recipe2": brain.search.by_key("Recipe2"),
        "Party": brain.search.by_key("Party"),
        "Guests": brain.search.by_key("Guests"),
    }


@pytest.fixture
def layout():
    return PlexLayout()


@pytest.fixture
def differ():
    return PlexStateDiff()
