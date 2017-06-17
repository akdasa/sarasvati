from .state_diff_line import PlexStateDiffLine
from .state import PlexState


class PlexStateDiff:
    @staticmethod
    def diff(old: PlexState, new: PlexState):
        """
        Return difference between two specified view states
        :param old: Old state
        :param new: New state
        :return: Array of PlexThoughtState
        """
        result = []
        ids = PlexStateDiff.get_ids(new, old)

        for tid in ids:
            old_state = old.get_state_by_thought_id(tid)
            new_state = new.get_state_by_thought_id(tid)
            thought = (old_state if old_state is not None else new_state).thought

            if old_state is None or new_state is None:  # add or remove thought
                old_state_name = old_state.state if old_state is not None else None
                new_state_name = new_state.state if new_state is not None else None
                result.append(PlexStateDiffLine(thought, old_state_name, new_state_name))
            elif old_state.state != new_state.state:  # change thought state
                result.append(PlexStateDiffLine(thought, old_state.state, new_state.state))
        return result

    @staticmethod
    def get_ids(new, old):
        ids = []
        for state in old.get_state():
            if state.thought.key not in ids:
                ids.append(state.thought.key)
        for state in new.get_state():
            if state.thought.key not in ids:
                ids.append(state.thought.key)
        return ids

