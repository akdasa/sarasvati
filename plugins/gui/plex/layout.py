from .layout_action import PlexLayoutAction
from .layout_placement import PlexLayoutPlacement
from .plex import PlexState
from .state_diff import PlexStateDiff


class PlexLayout:
    """Places nodes on plane"""
    def __init__(self):
        self.__prev = PlexState()
        self.__differ = PlexStateDiff()
        self.__np = PlexLayoutPlacement()  # thought placements for new state
        self.__pp = PlexLayoutPlacement()  # thought placements for previous state

    def change_to(self, state):
        """
        Changes plex layout to new one
        :type state: PlexState
        :param state: New layout state
        :return: Array of commands to change state to new
        """
        result = []

        # calculates placements for current and previous states
        self.__pp.place(self.__prev)
        self.__np.place(state)

        # calculate difference between previous and new state
        diffs = self.__differ.diff(self.__prev, state)
        for diff in diffs:
            if diff.old_state is None:  # new thought added
                self.__add_thought(diff, result)
            elif diff.new_state is None:  # old thought removed
                self.__remove_thought(diff, result)
            else:  # thought changes state
                self.__change_state(diff, result)
        self.__prev = state
        return result

    def __add_thought(self, diff, result):
        # append "add" action
        result.append(PlexLayoutAction(diff.thought, "add"))

        # set new thought to the parent's/child's position
        kind = ("child" if diff.new_state == "parent" else "parent")
        linked = self.__get_linked(diff.thought, kind)
        if linked:
            old_pos = self.__pp.get_pos(linked)
            result.append(PlexLayoutAction(diff.thought, "set_pos_to", old_pos))

        # move added thought to the new position
        pos = self.__np.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move_to", pos))

    def __remove_thought(self, diff, result):
        parent = self.__get_linked(diff.thought, "parent")
        if parent:  # move node to the parent's position
            pos = self.__np.get_pos(parent) or \
                  self.__pp.get_pos(parent)
            result.append(PlexLayoutAction(diff.thought, "move_to", pos))
        result.append(PlexLayoutAction(diff.thought, "remove"))

    def __change_state(self, diff, result):
        pos = self.__np.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move_to", pos))

    def __get_linked(self, thought, kind):
        linked = thought.links.by_kind(kind)
        for thought in linked:
            state = self.__prev.get_state_by_thought_id(thought.key)
            if state is not None:
                return state.thought
        return None
