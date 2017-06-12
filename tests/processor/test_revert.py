
def test_revert(api):
    api.processor.execute("/c new")
    api.processor.execute("/r")

    result = api.brain.search.by_title("new")
    assert len(result) == 0
