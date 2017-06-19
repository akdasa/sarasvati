from .state import PlexState


class Plex:
    """
    Plex is a slice of the brain
    """
    def activate(self, thought):
        """
        Activate thought
        :rtype: PlexState
        :type thought: Thought
        :param thought: Thought
        :return: State of the plex
        """
        state = PlexState()

        if thought:
            state.add(thought, "root")
            links = thought.links.all
            for link_key in links:
                link = links[link_key]
                state.add(link.destination, link.kind)
        return state
