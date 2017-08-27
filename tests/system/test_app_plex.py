
def test_create_and_activate(api, app):
    api.execute("/c Root")
    root = api.execute("/a Root").value

    plex_state = app.plex.state

    assert plex_state.by_state("root") == [root]


def test_create_and_activate_2(api, app):
    api.execute("/c Root")
    api.execute("/c Child parent:Root")
    root = api.execute("/a Root").value
    child = api.utilities.find_one_by_title("Child")

    plex_state = app.plex.state

    assert plex_state.by_state("root") == [root]
    assert plex_state.by_state("child") == [child]


def test_create_and_delete(app, script):
    """Deleted node not present in plex"""
    script([
        "/c Root",
        "/c Child parent:Root",
        "/a Root",
        "/d Child"])

    assert app.plex.state.by_state("child") == []
