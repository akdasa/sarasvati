from sarasvati.brain.model import Model


def test_init():
    model = Model()
    assert model.identity is not None


def test_init_with_specified_components(component):
    m = Model(components=[component])
    assert m.get_component("component") is not None


def test_key_generated():
    model = Model()
    assert model.key is not None
    assert model.key is not ""
    assert model.key is not 0


def test_key_unique():
    m1 = Model()
    m2 = Model()
    assert m1.key != m2.key


def test_key_returns_identity():
    model = Model()
    assert model.identity.key == model.key


def test_string_representation():
    model = Model()
    assert str(model) == "<Model:" + model.key + ">"
