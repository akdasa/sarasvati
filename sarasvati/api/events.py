from sarasvati.models import Component
from sarasvati.event import Event


class SarasvatiEventsApiComponent(Component):
    COMPONENT_NAME = "events"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.thought_activated = Event()
        self.thought_changed = Event()
        self.thought_changing = Event()
        self.message = Event()
