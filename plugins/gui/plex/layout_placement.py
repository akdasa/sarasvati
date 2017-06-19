from .state import PlexState


class PlexLayoutPlacement:
    def __init__(self):
        self.offset = {"child_x": 0, "parent_x": 0,"jump_y": 0}
        self.result = {}

    def place(self, plex_state: PlexState):
        self.offset = {"child_x": 0, "parent_x": 0,"jump_y": 0}
        self.result = {}
        for state in ["root", "parent", "child", "reference"]:
            thoughts = plex_state.get_thoughts_by_state(state)
            thoughts = sorted(thoughts, key=lambda t: t.title)

            pos = self.__get_pos(state, thoughts)
            self.result.update(
                pos
            )

            #for thought in sorted(thoughts, key=lambda t: t.title):
            #    pos = self.__get_pos(state)
            #    self.result[thought.key] = pos
        return self.result

    def get_pos(self, thought):
        return self.result.get(thought.key, None)

    @staticmethod
    def __get_pos(state, thoughts):
        if state == "root" and len(thoughts) > 0:
            return {thoughts[0].key: [0, 0]}

        result = {}
        if state in ["child", "parent"]:
            y = -100 if state == "parent" else 100
            count = min(3, len(thoughts))
            while count > 0:
                v = []
                for x in range(0, count):
                    v.append(thoughts.pop(0))

                if len(v) == 1:
                    result[v[0].key] = [0, y]
                else:
                    for idx, t in enumerate(v):
                        x = (200 / (len(v)-1))*idx
                        result[t.key] = [x-100, y]

                y += 50
                count = min(3, len(thoughts))

        if state in ["reference"]:
            y = 0
            for rt in thoughts:
                result[rt.key] = [-100, y]
                y -= 50

        return result





    def __get_pos_old(self, state):
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
