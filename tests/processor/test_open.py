
def test_open(api):
    api.processor.execute("/c unique_thought key:qwerty")
    assert api.brain.storage.get("qwerty") is not None

    api.processor.execute("/open test_db.json")
    assert api.brain.storage.get("qwerty") is None
