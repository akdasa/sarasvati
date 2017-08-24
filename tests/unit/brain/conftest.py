import pytest

from plugins.storage.local import LocalStorage
from sarasvati.brain import Brain, Thought
from sarasvati.commands import Command, Transaction
from sarasvati.models import Component
from sarasvati.serialization import IdentityComponentSerializer, DefinitionComponentSerializer, LinksComponentSerializer


class MyCommand(Command):
    def __init__(self, can_execute=True):
        super().__init__()
        self.executed = False
        self.reverted = False
        self.__can_execute = can_execute

    def execute(self):
        self.executed = True

    def revert(self):
        self.reverted = True

    def can_execute(self):
        return self.__can_execute

    def set_can_execute(self, value):
        self.__can_execute = value


class MyComponent(Component):
    def __init__(self, name):
        super().__init__(name)


@pytest.fixture(name="brain")
def __brain():
    st = LocalStorage(None)
    s = st.serializer

    s.register("identity", IdentityComponentSerializer())
    s.register("definition", DefinitionComponentSerializer())
    s.register("links", LinksComponentSerializer(st))

    return Brain(st)


@pytest.fixture(name="full_brain")
def __full_brain(brain):
    t1 = Thought(title="Thought one", description="desc")
    t2 = Thought(title="Thought two", description="other")
    brain.storage.add(t1)
    brain.storage.add(t2)
    return brain


@pytest.fixture()
def command():
    return MyCommand()


@pytest.fixture()
def component():
    return MyComponent("component")


@pytest.fixture(name="tri")
def __tri():
    return Transaction(), MyCommand(), MyCommand()
