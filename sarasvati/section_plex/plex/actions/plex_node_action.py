from api.event import Event
from ..node import PlexNode


class PlexNodeAction:
    def __init__(self, plex_node: PlexNode):
        self.completed = Event()
        self.node = plex_node
