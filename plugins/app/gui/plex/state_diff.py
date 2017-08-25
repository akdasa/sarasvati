from .state import PlexState
from .state_diff_line import PlexStateDiffLine


class PlexStateDiff:
    @staticmethod
    def diff(old: PlexState, new: PlexState, same=False):
        """
        Return difference between two specified view states
        :param same: Keep lines with no state changes
        :param old: Old state
        :param new: New state
        :return: Array of PlexThoughtState
        """
        result = []

        for key in PlexStateDiff.__get_keys(new, old):
            old_state = old.by_key(key)
            new_state = new.by_key(key)
            thought = (old_state if old_state else new_state).thought

            if not (old_state and new_state):  # add or remove thought
                old_state_name = old_state.state if old_state else None
                new_state_name = new_state.state if new_state else None
                result.append(PlexStateDiffLine(thought, old_state_name, new_state_name))
            elif old_state.state != new_state.state:  # change thought state
                result.append(PlexStateDiffLine(thought, old_state.state, new_state.state))
            elif same:
                result.append(PlexStateDiffLine(thought, old_state.state, new_state.state))
        return result

    @staticmethod
    def __get_keys(new, old):
        """Returns list of thought's keys used in both states"""
        a = [x.thought.key for x in new.get_state() + old.get_state()]
        return set(a)
