from sarasvati.models import Component
from sarasvati.event import Event


class SarasvatiEventsApiComponent(Component):
    COMPONENT_NAME = "events"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.activating = Event()
        self.activated = Event()

        self.changing = Event()
        self.changed = Event()
        self.deleted = Event()
        self.created = Event()

        self.message = Event()
