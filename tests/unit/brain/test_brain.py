def test_brain_init(brain):
    assert brain.commands is not None
    assert brain.search is not None
    assert brain.stats is not None
    assert brain.state is not None
    assert brain.storage is not None
