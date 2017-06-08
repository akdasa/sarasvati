from sarasvati.brain.model import Model, Component


def test_init_with_specified_components():
    c = Component(name="dummy")
    m = Model(components=[c])
    assert m.get_component("dummy") is not None


def test_key_generated():
    model = Model()
    assert model.key is not None
    assert model.key is not ""
    assert model.key is not 0


def test_key_unique():
    m1 = Model()
    m2 = Model()
    assert m1.key != m2.key


def test_identity_component_is_accessible():
    model = Model()
    assert model.identity is not None


def test_serialization_component_is_accessible():
    model = Model()
    assert model.serialization is not None


def test_key_returns_identity():
    model = Model()
    assert model.identity.key == model.key


def test_model_string_representation():
    model = Model()
    assert str(model) == "<Model:" + model.key + ">"


def test_model_basic_serialization():
    model = Model()
    assert model.serialization.serialize() == {"identity": {"key": model.key}}
