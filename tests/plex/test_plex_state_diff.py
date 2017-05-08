from sarasvati.section_plex.plex import PlexStateDiffLine


def test_activate_same_no_diff(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"])
    state2 = plex.activate(thoughts["Brain"])
    assert differ.diff(state1, state2) == []


def test_activate_root_and_child(plex, differ, thoughts):
    state1 = plex.activate(thoughts["Brain"])
    state2 = plex.activate(thoughts["Tasks"])
    expected = [
        PlexStateDiffLine(thoughts["Brain"], "root", "parent"),
        PlexStateDiffLine(thoughts["Task1"], None, "child"),
        PlexStateDiffLine(thoughts["Task2"], None, "child"),
        PlexStateDiffLine(thoughts["Recipes"], "child", None),
        PlexStateDiffLine(thoughts["Tasks"], "child", "root"),
    ]

    diff = differ.diff(state1, state2)
    assert __sort_by_id(diff) == __sort_by_id(expected)


# def test_activate_root_and_second_child(self):
#     state1 = self.plex.activate(self.root_thought)
#     state2 = self.plex.activate(self.second_child)
#     expected = [
#         PlexStateDiffLine(self.root_thought, "root", "parent"),
#         PlexStateDiffLine(self.first_child, "child", None),
#         PlexStateDiffLine(self.second_child, "child", "root")
#     ]
#     diff = self.differ.diff(state1, state2)
#
#     self.__sort_by_id(diff)
#     self.__sort_by_id(expected)
#     self.assertEqual(diff, expected)
#
# def test_activate_child_of_child_and_first_child(self):
#     state1 = self.plex.activate(self.child_of_child)
#     state2 = self.plex.activate(self.first_child)
#     expected = [
#         PlexStateDiffLine(self.root_thought, None, "parent"),
#         PlexStateDiffLine(self.first_child, "parent", "root"),
#         PlexStateDiffLine(self.child_of_child, "root", "child")
#     ]
#     diff = self.differ.diff(state1, state2)
#
#     self.__sort_by_id(diff)
#     self.__sort_by_id(expected)
#     self.assertEqual(diff, expected)
#

def __sort_by_id(array):
    return sorted(array, key=lambda t: t.thought.key)
