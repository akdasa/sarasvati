from api.brain import Thought
from . import PlexState


class PlexLayoutPlacement:
    def __init__(self):
        self.offset = {"child_x": 0, "parent_x": 0,"jump_y": 0}
        self.result = {}

    def place(self, plex_state: PlexState):
        self.offset = {"child_x": 0, "parent_x": 0,"jump_y": 0}
        self.result = {}
        for state in ["root", "parent", "child", "reference"]:
            thoughts = plex_state.get_thoughts_by_state(state)
            for thought in sorted(thoughts, key=lambda t: t.title):
                pos = self.__get_pos(state)
                self.result[thought.key] = pos
        return self.result

    def get_pos(self, thought: Thought):
        return self.result[thought.key]

    def __get_pos(self, state):
        if state == "root":
            return [0, 0]

        if state == "parent":
            x = self.offset["parent_x"]
            self.offset["parent_x"] += 100
            return [x, -100]

        if state == "child":
            x = self.offset["child_x"]
            x += 100
            self.offset["child_x"] += 100
            return [x, 100]

        if state == "reference":
            y = self.offset["jump_y"]
            self.offset["jump_y"] -= 40
            return [-200, y]
