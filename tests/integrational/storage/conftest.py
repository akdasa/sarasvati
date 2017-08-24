import pytest

from sarasvati.brain import Thought


@pytest.fixture
def thought():
    return Thought("Root", key="Root")


@pytest.fixture
def empty_storage(api):
    return api.storage
