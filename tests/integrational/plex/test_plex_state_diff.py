from plugins.app.gui.plex import PlexStateDiffLine


def test_activate_same_no_diff(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"]).state
    state2 = plex.activate(thoughts["Brain"]).state
    assert differ.diff(state1, state2) == []


def test_activate_root_and_child(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"]).state
    state2 = plex.activate(thoughts["Tasks"]).state
    assert _s(differ.diff(state1, state2)) == _s([
        PlexStateDiffLine(thoughts["Brain"], "root", "parent"),
        PlexStateDiffLine(thoughts["Task1"], None, "child"),
        PlexStateDiffLine(thoughts["Task2"], None, "child"),
        PlexStateDiffLine(thoughts["Recipes"], "child", None),
        PlexStateDiffLine(thoughts["Tasks"], "child", "root"),
    ])


def test_activate_root_and_task1(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"]).state
    state2 = plex.activate(thoughts["Task1"]).state
    assert _s(differ.diff(state1, state2)) == _s([
        PlexStateDiffLine(thoughts["Brain"], "root", None),
        PlexStateDiffLine(thoughts["Recipes"], "child", None),
        PlexStateDiffLine(thoughts["Task1"], None, "root"),
        PlexStateDiffLine(thoughts["Tasks"], "child", "parent"),
    ])


def test_activate_root_and_task2(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"]).state
    state2 = plex.activate(thoughts["Task2"]).state
    assert _s(differ.diff(state1, state2)) == _s([
        PlexStateDiffLine(thoughts["Brain"], "root", None),
        PlexStateDiffLine(thoughts["Party"], None, "parent"),
        PlexStateDiffLine(thoughts["Task2"], None, "root"),
        PlexStateDiffLine(thoughts["Tasks"], "child", "parent"),
        PlexStateDiffLine(thoughts["Recipe1"], None, "reference"),
        PlexStateDiffLine(thoughts["Recipes"], "child", None),
    ])


def test_activate_root_and_party(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"]).state
    state2 = plex.activate(thoughts["Party"]).state
    assert _s(differ.diff(state1, state2)) == _s([
        PlexStateDiffLine(thoughts["Brain"], "root", None),
        PlexStateDiffLine(thoughts["Party"], None, "root"),
        PlexStateDiffLine(thoughts["Tasks"], "child", None),
        PlexStateDiffLine(thoughts["Recipes"], "child", None),
        PlexStateDiffLine(thoughts["Guests"], None, "child"),
        PlexStateDiffLine(thoughts["Task2"], None, "child")
    ])


def test_activate_root_and_recipe1(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"]).state
    state2 = plex.activate(thoughts["Recipe1"]).state
    assert _s(differ.diff(state1, state2)) == _s([
        PlexStateDiffLine(thoughts["Brain"], "root", None),
        PlexStateDiffLine(thoughts["Tasks"], "child", None),
        PlexStateDiffLine(thoughts["Task2"], None, "reference"),
        PlexStateDiffLine(thoughts["Recipe1"], None, "root"),
        PlexStateDiffLine(thoughts["Recipes"], "child", "parent")
    ])


def _s(array):
    return sorted(array, key=lambda t: t.thought.key)
