import pytest

from api.brain import Brain
from sarasvati.section_plex.plex import Plex, PlexLayout, PlexStateDiff
from sarasvati.storage_local import LocalStorage


@pytest.fixture
def brain():
    storage = LocalStorage("./tests/plex/fixtures/full_brain.json")
    return Brain(storage)


@pytest.fixture
def plex(brain):
    return Plex(brain)


@pytest.fixture
def thoughts(brain):
    # Brain -> Tasks
    # Brain -> Recipes
    # Tasks -> Task1
    # Tasks -> Task2
    # Task2 -> Recipe1
    # Recipes -> Recipe1
    # Recipes -> Recipe2
    # Recipe1 <-> Task1
    return {
        "Brain": brain.search.by_id("Brain"),
        "Tasks": brain.search.by_id("Tasks"),
        "Recipes": brain.search.by_id("Recipes"),
        "Task1": brain.search.by_id("Read 'Alice in wunderland'"),
        "Task2": brain.search.by_id("Cook cake"),
        "Recipe1": brain.search.by_id("Recipe 'Anthill cake'"),
        "Recipe2": brain.search.by_id("Simple wounderful"),
        "Party": brain.search.by_id("Party"),
        "Guests": brain.search.by_id("Guests"),
    }


@pytest.fixture
def layout():
    return PlexLayout()


@pytest.fixture
def differ():
    return PlexStateDiff()
