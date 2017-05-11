from sarasvati.section_plex.plex import PlexLayoutAction


def test_root(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    assert compare(layout.change_to(state), [
        PlexLayoutAction(thoughts["Brain"], "add", None),
        PlexLayoutAction(thoughts["Brain"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Tasks"], "add", None),
        PlexLayoutAction(thoughts["Tasks"], "move_to",  [100, 100]),
        PlexLayoutAction(thoughts["Recipes"], "add", None),
        PlexLayoutAction(thoughts["Recipes"], "move_to", [200, 100])
    ])


def test_tasks(plex, layout, thoughts):
    state = plex.activate(thoughts["Tasks"])
    assert compare(layout.change_to(state), [
        PlexLayoutAction(thoughts["Tasks"], "add", None),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Brain"], "add", None),
        PlexLayoutAction(thoughts["Brain"], "move_to", [0, -100]),
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "move_to", [100, 100]),
        PlexLayoutAction(thoughts["Task2"], "add", None),
        PlexLayoutAction(thoughts["Task2"], "move_to", [200, 100])
    ])


def test_task1(plex, layout, thoughts):
    state = plex.activate(thoughts["Task1"])
    assert compare(layout.change_to(state), [
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Tasks"], "add", None),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, -100]),
    ])


def test_brain_and_tasks(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    layout.change_to(state)
    state = plex.activate(thoughts["Tasks"])

    assert compare(layout.change_to(state), [
        PlexLayoutAction(thoughts["Brain"], "move_to", [0, -100]),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Recipes"], "move_to", thoughts["Brain"]),
        PlexLayoutAction(thoughts["Recipes"], "remove", None),
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "set_pos_to", thoughts["Tasks"]),
        PlexLayoutAction(thoughts["Task1"], "move_to", [100, 100]),
        PlexLayoutAction(thoughts["Task2"], "add", None),
        PlexLayoutAction(thoughts["Task2"], "set_pos_to", thoughts["Tasks"]),
        PlexLayoutAction(thoughts["Task2"], "move_to", [200, 100])
    ])


def test_brain_and_tasks1(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    layout.change_to(state)
    state = plex.activate(thoughts["Task1"])

    assert compare(layout.change_to(state), [
        PlexLayoutAction(thoughts["Brain"], "remove"),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, -100]),
        PlexLayoutAction(thoughts["Recipes"], "move_to", thoughts["Brain"]),
        PlexLayoutAction(thoughts["Recipes"], "remove"),
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "set_pos_to", thoughts["Tasks"]),
        PlexLayoutAction(thoughts["Task1"], "move_to", [0, 0]),
    ])


def test_twice_empty(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    layout.change_to(state)
    state = plex.activate(thoughts["Brain"])
    assert layout.change_to(state) == []


def compare(array1, array2):
    return sorted(array1, key=lambda a: a.thought.key) == sorted(array2, key=lambda a: a.thought.key)