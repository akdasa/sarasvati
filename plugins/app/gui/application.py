from sarasvati.application import SarasvatiApplication
from .client import Client
from .controllers import *


class SarasvatiGuiApplication(SarasvatiApplication):
    def __init__(self, brain_path="db.json"):
        super().__init__()
        self._api.open_brain(brain_path)

        self.plex = PlexController()
        self.processor = ProcessorController()
        self.brain = BrainController()

        self.__client = Client(self._api, controllers={
            "processor": self.processor,
            "brain": self.brain,
            "plex": self.plex
        })

    def run(self):
        self.__client.run()
