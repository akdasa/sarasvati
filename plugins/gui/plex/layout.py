from sarasvati.brain import LinkType
from .layout_action import PlexLayoutAction
from .layout_placement import PlexLayoutPlacement
from .plex import PlexState
from .state_diff import PlexStateDiff


class PlexLayout:
    """Places nodes on plane"""

    def __init__(self):
        self.__prev = PlexState()
        self.__state = PlexState()
        self.__differ = PlexStateDiff()
        self.__np = PlexLayoutPlacement()  # thought placements for new state
        self.__pp = PlexLayoutPlacement()  # thought placements for previous state
        self.__state_idx = 0

    def change_to(self, state):
        """
        Changes plex layout to new one
        :type state: PlexState
        :param state: New layout state
        :return: Array of commands to change state to new
        """
        result = []
        self.__state = state

        # calculates placements for current and previous states
        self.__pp.place(self.__prev)
        self.__np.place(state)

        # calculate difference between states
        diffs = self.__differ.diff(self.__prev, state)
        for diff in diffs:
            if diff.old_state is None:  # new thought added
                self.__add(diff, result)
            elif diff.new_state is None:  # old thought removed
                self.__remove(diff, result)
            else:  # thought changes state
                self.__change(diff, result)

        self.__prev = state
        self.__state_idx += 1
        return result

    def __add(self, diff, result):
        if diff.new_state == "root":
            data = {"pos": [0, 0]}
        else:
            opposite = LinkType.opposite(diff.new_state)
            linked = self.__linked(diff.thought, opposite)
            pos = self.__p().get_pos(linked)
            data = {"pos": pos, "key": linked.key}

        result.append(PlexLayoutAction(diff.thought, "add", data))
        self.__move(diff.thought, result, not_to=data["pos"])

    def __change(self, diff, result):
        pos = self.__np.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move", pos))

    def __remove(self, diff, result):
        action = PlexLayoutAction(diff.thought, "remove")

        if diff.old_state == "root":
            action.data = None
        else:
            opposite = LinkType.opposite(diff.old_state)
            linked = self.__linked(diff.thought, opposite)
            new_pos = self.__np.get_pos(linked)
            if new_pos:
                result.append(PlexLayoutAction(diff.thought, "move", new_pos))

        result.append(action)
        self.__move(diff.thought, result)

    def __move(self, thought, result, not_to=None):
        pos = self.__np.get_pos(thought)
        if pos and pos != not_to:
            result.append(PlexLayoutAction(thought, "move", pos))

    def __linked(self, thought, kind=None):
        linked = thought.links.by_kind(kind) if kind else thought.links.all
        linked_on_board = [x for x in linked if self.__s().get_state_by_thought_id(x.key)]
        linked_on_board_s = sorted(linked_on_board, key=lambda x: (self.__np.distance(thought, x) or 9999, x.key))
        if linked_on_board_s:
            return linked_on_board[0]

    def __s(self):
        return self.__state if self.__state_idx == 0 else self.__prev

    def __p(self):
        return self.__np if self.__state_idx == 0 else self.__pp
