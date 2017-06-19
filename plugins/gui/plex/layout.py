from sarasvati.brain import LinkType
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
        opposite = LinkType.opposite(diff.new_state)
        linked = self.__linked(diff.thought, opposite)
        if linked:
            old_pos = self.__pp.get_pos(linked)
            result.append(PlexLayoutAction(diff.thought, "set_pos_to", old_pos))

        # move added thought to the new position
        pos = self.__np.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move_to", pos))

    def __remove_thought(self, diff, result):
        # move removing thought to linked thought
        opposite = LinkType.opposite(diff.new_state)
        linked = self.__linked(diff.thought, opposite)
        if linked:  # move node to the linked thought
            pos = self.__np.get_pos(linked) or \
                  self.__pp.get_pos(linked)
            result.append(PlexLayoutAction(diff.thought, "move_to", pos))
        result.append(PlexLayoutAction(diff.thought, "remove"))

    def __change_state(self, diff, result):
        pos = self.__np.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move_to", pos))

    def __linked(self, thought, kind=None):
        linked = thought.links.by_kind(kind) if kind else thought.links.all

        for thought in linked:
            state = self.__prev.get_state_by_thought_id(thought.key)
            if state is not None:
                return state.thought
        return None
