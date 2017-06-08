import pytest

from sarasvati.brain import Thought
from plugins.storage_local import LocalStorage


@pytest.fixture
def root_thought():
    return Thought("Root", key="Root")


@pytest.fixture
def storage():
    return LocalStorage("./tests/storage_local/fixtures/full_brain.json")


@pytest.fixture
def thoughts(storage):
    # Brain -> Tasks
    # Brain -> Recipes
    # Tasks -> Task1
    # Tasks -> Task2
    # Task2 -> Recipe1
    # Recipes -> Recipe1
    # Recipes -> Recipe2
    # Recipe1 <-> Task1
    return {
        "Brain": storage.get("Brain"),
        "Tasks": storage.get("Tasks"),
        "Recipes": storage.get("Recipes"),
        "Task1": storage.get("Read 'Alice in wunderland'"),
        "Task2": storage.get("Cook cake"),
        "Recipe1": storage.get("Recipe 'Anthill cake'"),
        "Recipe2": storage.get("Simple wounderful"),
        "Party": storage.get("Party"),
        "Guests": storage.get("Guests"),
    }


@pytest.fixture
def empty_storage():
    return LocalStorage(None)

