
def test_revert(api):
    api.processor.execute("/c new")
    api.processor.execute("/r")

    result = api.brain.search.by_title("new")
    assert len(result) == 0


def test_revert_deleted(api):
    root = api.processor.execute("/c root").value
    child = api.processor.execute("/c child parent:root").value
    api.processor.execute("/d child")
    api.processor.execute("/r")

    assert child in root.links.children
    assert root in child.links.parents
