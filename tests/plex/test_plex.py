
def test_activate_brain(plex, thoughts, compare):
    state = plex.activate(thoughts["Brain"])
    assert compare(state.get_thoughts_by_state("root"), [thoughts["Brain"]])
    assert compare(state.get_thoughts_by_state("child"), [thoughts["Tasks"], thoughts["Recipes"]])
    assert compare(state.get_thoughts_by_state("parent"), [])
    assert compare(state.get_thoughts_by_state("reference"), [])
    assert len(state.get_state()) == 3


def test_activate_tasks(plex, thoughts, compare):
    state = plex.activate(thoughts["Tasks"])
    assert compare(state.get_thoughts_by_state("root"), [thoughts["Tasks"]])
    assert compare(state.get_thoughts_by_state("child"), [thoughts["Task1"], thoughts["Task2"]])
    assert compare(state.get_thoughts_by_state("parent"), [thoughts["Brain"]])
    assert compare(state.get_thoughts_by_state("reference"), [])
    assert len(state.get_state()) == 4


def test_activate_task1(plex, thoughts, compare):
    state = plex.activate(thoughts["Task1"])
    assert compare(state.get_thoughts_by_state("root"), [thoughts["Task1"]])
    assert compare(state.get_thoughts_by_state("child"), [])
    assert compare(state.get_thoughts_by_state("parent"), [thoughts["Tasks"]])
    assert compare(state.get_thoughts_by_state("reference"), [])
    assert len(state.get_state()) == 2


def test_activate_task2(plex, thoughts, compare):
    state = plex.activate(thoughts["Task2"])
    assert compare(state.get_thoughts_by_state("root"), [thoughts["Task2"]])
    assert compare(state.get_thoughts_by_state("child"), [])
    assert compare(state.get_thoughts_by_state("parent"), [thoughts["Tasks"]])
    assert compare(state.get_thoughts_by_state("reference"), [thoughts["Recipe1"]])
    assert len(state.get_state()) == 3


def test_activate_recipe1(plex, thoughts, compare):
    state = plex.activate(thoughts["Recipe1"])
    assert compare(state.get_thoughts_by_state("root"), [thoughts["Recipe1"]])
    assert compare(state.get_thoughts_by_state("child"), [])
    assert compare(state.get_thoughts_by_state("parent"), [thoughts["Recipes"]])
    assert compare(state.get_thoughts_by_state("reference"), [thoughts["Task2"]])
    assert len(state.get_state()) == 3


def test_activate_recipe2(plex, thoughts, compare):
    state = plex.activate(thoughts["Recipe2"])
    assert compare(state.get_thoughts_by_state("root"), [thoughts["Recipe2"]])
    assert compare(state.get_thoughts_by_state("child"), [])
    assert compare(state.get_thoughts_by_state("parent"), [thoughts["Recipes"]])
    assert compare(state.get_thoughts_by_state("reference"), [])
    assert len(state.get_state()) == 2

