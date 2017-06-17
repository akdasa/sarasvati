from sarasvati.brain.model import Component
from sarasvati.commands import CommandException
from sarasvati.event import Event


class SarasvatiEventsApiComponent(Component):
    COMPONENT_NAME = "events"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.thought_activated = Event()