from math import sqrt, pow

from .state import PlexState


class PlexLayoutPlacement:
    def __init__(self):
        self.__offset = {"child_x": 0, "parent_x": 0, "jump_y": 0}
        self.__result = {}

    def place(self, plex_state: PlexState):
        self.__offset = {"child_x": 0, "parent_x": 0, "jump_y": 0}
        self.__result = {}
        for state in ["root", "parent", "child", "reference"]:
            thoughts = plex_state.get_thoughts_by_state(state)
            thoughts = sorted(thoughts, key=lambda t: t.title)

            pos = self.__get_pos(state, thoughts)
            self.__result.update(pos)

        return self.__result

    def get_pos(self, thought):
        return self.__result.get(thought.key, None)

    def distance(self, t1, t2):
        pos1 = self.get_pos(t1)
        pos2 = self.get_pos(t2)

        if pos1 and pos2:
            return sqrt(pow(pos2[0]-pos1[0], 2) + pow(pos2[1]-pos1[1], 2))

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


