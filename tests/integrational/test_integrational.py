
def test_delete_and_revert(api):
    api.execute("/c 1")
    api.execute("/c 2 parent:1")
    api.execute("/d 2")
    api.execute("/r")

    api.brain.storage.cache.clear()

    thought = api.execute("/a 1").value
    assert len(thought.links.all) == 1

    thought = api.execute("/a 2").value
    assert len(thought.links.all) == 1
