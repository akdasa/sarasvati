
def test_open(api):
    api.execute("/c unique_thought key:qwerty")
    assert api.brain.storage.get("qwerty") is not None

    api.execute("/open test_db.json")
    assert api.brain.storage.get("qwerty") is None
