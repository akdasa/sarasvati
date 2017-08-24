import pytest


@pytest.fixture(name="storage")
def __storage(api):
    api.execute("/c Brain key:Brain")
    api.execute("/c Tasks parent:Brain key:Tasks")
    api.execute("/c Recipes parent:Brain key:Recipes")
    api.execute("/c Read 'Alice in wunderland' parent:Tasks key:Task1")
    api.execute("/c Cook cake parent:Tasks key:Task2")
    api.execute("/c Anthill cake parent:Recipes key:Recipe1")
    api.execute("/c Simple wounderful parent:Recipes key:Recipe2")
    api.execute("/c Party key:Party")
    api.execute("/c Guests parent:Party key:Guests")
    api.execute("/l Cook cake to:Party as:child")
    api.execute("/l Cook cake to:Anthill cake as:reference")

    api.storage.cache.clear()

    return api.storage
