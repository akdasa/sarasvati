
def test_activate_brain(plex, thoughts):
    state = plex.activate(thoughts["Brain"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Brain"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([thoughts["Tasks"], thoughts["Recipes"]])
    assert _s(state.get_thoughts_by_state("parent")) == _s([])
    assert _s(state.get_thoughts_by_state("reference")) == _s([])
    assert len(state.get_state()) == 3


def test_activate_tasks(plex, thoughts):
    state = plex.activate(thoughts["Tasks"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Tasks"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([thoughts["Task1"], thoughts["Task2"]])
    assert _s(state.get_thoughts_by_state("parent")) == _s([thoughts["Brain"]])
    assert _s(state.get_thoughts_by_state("reference")) == _s([])
    assert len(state.get_state()) == 4


def test_activate_task1(plex, thoughts):
    state = plex.activate(thoughts["Task1"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Task1"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([])
    assert _s(state.get_thoughts_by_state("parent")) == _s([thoughts["Tasks"]])
    assert _s(state.get_thoughts_by_state("reference")) == _s([])
    assert len(state.get_state()) == 2


def test_activate_task2(plex, thoughts):
    state = plex.activate(thoughts["Task2"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Task2"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([])
    assert _s(state.get_thoughts_by_state("parent")) == _s([thoughts["Tasks"], thoughts["Party"]])
    assert _s(state.get_thoughts_by_state("reference")) == _s([thoughts["Recipe1"]])
    assert len(state.get_state()) == 4


def test_activate_recipe1(plex, thoughts):
    state = plex.activate(thoughts["Recipe1"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Recipe1"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([])
    assert _s(state.get_thoughts_by_state("parent")) == _s([thoughts["Recipes"]])
    assert _s(state.get_thoughts_by_state("reference")) == _s([thoughts["Task2"]])
    assert len(state.get_state()) == 3


def test_activate_recipe2(plex, thoughts):
    state = plex.activate(thoughts["Recipe2"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Recipe2"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([])
    assert _s(state.get_thoughts_by_state("parent")) == _s([thoughts["Recipes"]])
    assert _s(state.get_thoughts_by_state("reference")) == _s([])
    assert len(state.get_state()) == 2


def test_activate_party(plex, thoughts):
    state = plex.activate(thoughts["Party"])
    assert _s(state.get_thoughts_by_state("root")) == _s([thoughts["Party"]])
    assert _s(state.get_thoughts_by_state("child")) == _s([thoughts["Task2"], thoughts["Guests"]])
    assert _s(state.get_thoughts_by_state("parent")) == _s([])
    assert _s(state.get_thoughts_by_state("reference")) == _s([])
    assert len(state.get_state()) == 3


def _s(array1):
    return sorted(array1, key=lambda t: t.key)
