import pytest

from plugins.gui.plex import Plex, PlexLayout, PlexStateDiff
from sarasvati.brain import Brain


@pytest.fixture
def storage(api):
    api.processor.execute("/c Brain key:Brain")
    api.processor.execute("/c Tasks parent:Brain key:Tasks")
    api.processor.execute("/c Recipes parent:Brain key:Recipes")
    api.processor.execute("/c Read 'Alice in wunderland' parent:Tasks key:Task1")
    api.processor.execute("/c Cook cake parent:Tasks key:Task2")
    api.processor.execute("/c Anthill cake parent:Recipes key:Recipe1")
    api.processor.execute("/c Simple wounderful parent:Recipes key:Recipe2")
    api.processor.execute("/c Party key:Party")
    api.processor.execute("/c Guests parent:Party key:Guests")
    api.processor.execute("/l Cook cake to:Party as:child")
    api.processor.execute("/l Cook cake to:Anthill cake as:reference")

    return api.storage


@pytest.fixture
def brain(storage):
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
