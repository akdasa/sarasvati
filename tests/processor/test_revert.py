
def test_revert(api):
    api.execute("/c new")
    api.execute("/r")

    result = api.brain.search.by_title("new")
    assert len(result) == 0


def test_revert_deleted(api):
    root = api.execute("/c root").value
    child = api.execute("/c child parent:root").value
    api.execute("/d child")
    api.execute("/r")

    assert child in root.links.children
    assert root in child.links.parents


def test_revert_history(api):
    api.execute("/c root")
    api.execute("/c child parent:root")
    history = api.execute("/r h").value
    assert history == api.brain.commands.history


def test_revert_activate(api):
    api.execute("/c root")
    api.execute("/a root")
    api.execute("/r")
    assert api.brain.state.active_thought is None


def test_revert_update(api):
    api.execute("/c root")
    api.execute("/a root")
    api.execute("/u root title:new_t desc:new_d")
    api.execute("/r")
    api.execute("/r")
    assert api.brain.state.active_thought.title == "root"
    assert api.brain.state.active_thought.description is None


def test_revert_link(api):
    parent = api.execute("/c parent").value
    child = api.execute("/c child").value
    api.execute("/l child to:parent as:child")
    api.execute("/r")
    assert len(parent.links.all) == 0
    assert len(child.links.all) == 0


def test_revert_transaction_create_1(api):
    api.execute("/c parent")
    api.execute("/c child parent:parent desc:some desc")
    api.execute("/r")
    assert len(api.brain.commands.history) == 1


def test_revert_transaction_create_2(api):
    api.execute("/c parent desc:some desc")
    api.execute("/c child parent:parent desc:some desc")
    api.execute("/r")
    assert len(api.brain.commands.history) != 0

    api.execute("/r")
    assert len(api.brain.commands.history) == 0


def test_revert_transaction_create_3(api):
    api.execute("/c parent desc:some desc")
    api.execute("/c child1 parent:parent")
    api.execute("/c child2 parent:parent")

    api.execute("/r")
    assert len(api.brain.commands.history) == 4  # (create + link) * 2

    api.execute("/r")
    assert len(api.brain.commands.history) == 2  # create + link

    api.execute("/r")
    assert len(api.brain.commands.history) == 0  # no commands
