import pytest

from plugins.storage.local import LocalStorage
from sarasvati.brain import Brain
from sarasvati.serialization import IdentityComponentSerializer, DefinitionComponentSerializer, LinksComponentSerializer


@pytest.fixture()
def brain():
    st = LocalStorage(None)
    s = st.serializer

    s.register("identity", IdentityComponentSerializer())
    s.register("definition", DefinitionComponentSerializer())
    s.register("links", LinksComponentSerializer(st))

    return Brain(st)
