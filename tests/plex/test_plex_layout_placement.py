# import unittest
#
# from api.models import Thought
# from plugins.brain.plex import PlexLayoutPlacement, PlexState
# # noinspection PyUnresolvedReferences
# from assets import MemoryStorage
#
#
# class TestPlexLayoutPlacement(unittest.TestCase):
#     def setUp(self):
#         self.placement = PlexLayoutPlacement()
#         self.state = PlexState()
#         self.root = Thought("root")
#         self.child1 = Thought("child1")
#         self.child2 = Thought("child2")
#         self.parent1 = Thought("parent1")
#         self.jump1 = Thought("jump1")
#
#         self.child_offset = self.placement.get_section_offset("child")
#
#     def test_root(self):
#         self.state.add(self.root, "root")
#         self.placement.place(self.state)
#
#         self.assertEqual(self.placement.get_pos(self.root), [0, 0])
#
#     def test_root_and_child1(self):
#         self.state.add(self.root, "root")
#         self.state.add(self.child1, "child")
#         self.placement.place(self.state)
#
#         self.assertEqual(self.placement.get_pos(self.root), [0, 0])
#         self.assertEqual(self.placement.get_pos(self.child1), [0, self.child_offset[1]])