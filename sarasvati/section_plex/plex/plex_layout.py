from .plex import PlexState
from .plex_state_diff import PlexStateDiff
from .plex_layout_action import PlexLayoutAction
from .plex_layout_placement import PlexLayoutPlacement


class PlexLayout:
    def __init__(self):
        self.old_state = PlexState()
        self.state = PlexState()
        self.differ = PlexStateDiff()
        self.placement = PlexLayoutPlacement()

    def change_to(self, new_state) -> []:
        result = []
        self.placement.place(new_state)
        diffs = self.differ.diff(self.old_state, new_state)
        for diff in diffs:
            if diff.old_state is None:  # new thought added
                self.add_thought(diff, result)
            elif diff.new_state is None:  # old thought removed
                self.remove_thought(diff, result)
            else:  # thought changes state
                self.change_state(diff, result)
        self.old_state = new_state
        return result

    def add_thought(self, diff, result):
        result.append(PlexLayoutAction(diff.thought, "add"))

        kind = ("child" if diff.new_state == "parent" else "parent")
        linked_thought = self.get_linked(diff.thought, kind)
        if linked_thought:
            result.append(PlexLayoutAction(diff.thought, "set_pos_to", linked_thought))

        pos = self.placement.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move_to", pos))

    def remove_thought(self, diff, result):
        parent = self.get_linked(diff.thought, "parent")
        if parent:
            result.append(PlexLayoutAction(diff.thought, "move_to", parent))
        result.append(PlexLayoutAction(diff.thought, "remove"))

    def change_state(self, diff, result):
        pos = self.placement.get_pos(diff.thought)
        result.append(PlexLayoutAction(diff.thought, "move_to", pos))

    def get_linked(self, thought, kind):
        parents = thought.links.by_kind(kind)
        for parent in parents:
            tid = parent.key
            state = self.old_state.get_state_by_thought_id(tid)
            if state is not None:
                return state.thought
        return None
