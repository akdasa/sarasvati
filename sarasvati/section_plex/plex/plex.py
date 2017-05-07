from .plex_state import PlexState


class Plex:
    """
    Plex is a slice of the brain
    """
    def __init__(self, brain):
        """
        Initializes new instance of the Brain class
        :type brain: Brain
        :param brain: Brain to get data from
        """
        self.brain = brain


    def activate(self, thought):
        """
        Activate thought
        :rtype: PlexState
        :type thought: Thought
        :param thought: Thought
        :return: State of the plex
        """
        state = PlexState()
        state.add(thought, "root")

        links = thought.links.all
        for link_key in links:
            link = links[link_key]
            #loading_thought_key = link.destination.key
            #loaded_thought = self.brain.get_thought(loading_thought_key)
            state.add(link.destination, link.kind)

        return state
