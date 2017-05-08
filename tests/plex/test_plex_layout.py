# def setUp(self):
#     self.storage = MemoryStorage()
#     self.brain = Brain(self.storage)
#     self.plex = Plex(self.brain)
#     self.layout = PlexLayout()
#
#     # root -> 1child -> child_of_child
#     # root -> 2child
#     self.root = self.brain.create_thought("root")
#     self.child1 = self.brain.create_linked_thought(self.root, "parent->child", "1child")
#     self.child2 = self.brain.create_linked_thought(self.root, "parent->child", "2child")
#     self.child3 = self.brain.create_linked_thought(self.child1, "parent->child", "3child")
from sarasvati.section_plex.plex import PlexLayout, PlexLayoutAction


def test_root(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    assert layout.change_to(state) == [
        PlexLayoutAction(thoughts["Brain"], "add", None),
        PlexLayoutAction(thoughts["Brain"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Tasks"], "add", None),
        PlexLayoutAction(thoughts["Tasks"], "move_to",  [100, 100]),
        PlexLayoutAction(thoughts["Recipes"], "add", None),
        PlexLayoutAction(thoughts["Recipes"], "move_to", [200, 100])
    ]


def test_tasks(plex, layout, thoughts):
    state = plex.activate(thoughts["Tasks"])
    assert layout.change_to(state) == [
        PlexLayoutAction(thoughts["Tasks"], "add", None),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Brain"], "add", None),
        PlexLayoutAction(thoughts["Brain"], "move_to", [0, -100]),
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "move_to", [100, 100]),
        PlexLayoutAction(thoughts["Task2"], "add", None),
        PlexLayoutAction(thoughts["Task2"], "move_to", [200, 100])
    ]


def test_task1(plex, layout, thoughts):
    state = plex.activate(thoughts["Task1"])
    assert layout.change_to(state) == [
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "move_to", [0, 0]),
        PlexLayoutAction(thoughts["Tasks"], "add", None),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, -100]),
    ]


def test_brain_and_tasks(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    layout.change_to(state)
    state = plex.activate(thoughts["Tasks"])

    assert layout.change_to(state) == [
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
    ]


def test_brain_and_tasks1(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    layout.change_to(state)
    state = plex.activate(thoughts["Task1"])

    assert layout.change_to(state) == [
        PlexLayoutAction(thoughts["Brain"], "remove"),
        PlexLayoutAction(thoughts["Tasks"], "move_to", [0, -100]),
        PlexLayoutAction(thoughts["Recipes"], "move_to", thoughts["Brain"]),
        PlexLayoutAction(thoughts["Recipes"], "remove"),
        PlexLayoutAction(thoughts["Task1"], "add", None),
        PlexLayoutAction(thoughts["Task1"], "set_pos_to", thoughts["Tasks"]),
        PlexLayoutAction(thoughts["Task1"], "move_to", [0, 0]),
    ]


def test_twice_empty(plex, layout, thoughts):
    state = plex.activate(thoughts["Brain"])
    layout.change_to(state)
    state = plex.activate(thoughts["Brain"])
    assert layout.change_to(state) == []
