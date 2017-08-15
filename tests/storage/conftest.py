import pytest

from sarasvati.brain import Thought
from plugins.storage import LocalStorage


@pytest.fixture
def root_thought():
    return Thought("Root", key="Root")


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

    api.storage.cache.clear()

    return api.storage


@pytest.fixture
def empty_storage():
    return LocalStorage(None)

