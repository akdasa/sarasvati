from plugins.app.gui.plex import PlexLayoutAction


def test_create_and_activate(api, app):
    api.execute("/c Root")
    root = api.execute("/a Root").value

    plex_state = app.plex.plex.state

    assert plex_state.by_state("root") == [root]


def test_create_and_activate_2(api, app):
    api.execute("/c Root")
    api.execute("/c Child parent:Root")
    root = api.execute("/a Root").value
    child = api.utilities.find_one_by_title("Child")

    plex_state = app.plex.plex.state

    assert plex_state.by_state("root") == [root]
    assert plex_state.by_state("child") == [child]


def test_create_and_delete(app, script):
    """Deleted node not present in plex"""
    script([
        "/c Root",
        "/c Child parent:Root",
        "/a Root",
        "/d Child"])

    assert app.plex.plex.state.by_state("child") == []


def test_create_new_child(app, script):
    """Nodes should be moved to new position after new node created"""
    last_actions = None

    def __changed(state, actions):
        nonlocal last_actions
        last_actions = actions

    # let's receive actions passed to plex in __changed function
    app.plex.changed.subscribe(__changed)

    script([
        "/c Root key:Root",
        "/c Child key:Child parent:Root",
        "/a Root",
        "/c Child2 key:Child2 parent:Root"])

    root = app.api.storage.get("Root")
    child1 = app.api.storage.get("Child")
    child2 = app.api.storage.get("Child2")

    assert __s(last_actions) == __s([
        PlexLayoutAction(root, "move", [0, 0]),
        PlexLayoutAction(child1, "move", [-100, 100]),
        PlexLayoutAction(child2, "move", [100, 100]),
    ])


def __s(a):
    return sorted(a, key=lambda a: (a.thought.key, a.name, a.data))
