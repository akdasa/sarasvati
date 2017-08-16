import logging
import os

from sarasvati import set_api
from sarasvati.api.events import SarasvatiEventsApiComponent
from sarasvati.api.plugins import SarasvatiPluginsApiComponent
from sarasvati.api.serialization import SarasvatiSerializationApiComponent
from sarasvati.api.utilities import SarasvatiUtilitiesApiComponent
from sarasvati.brain import Brain
from sarasvati.models import Composite


class SarasvatiApi(Composite):
    def __init__(self):
        set_api(self)
        super().__init__()

        self.brain = None
        self.execute = None  # todo Convert to method

        self.add_components([
            SarasvatiPluginsApiComponent(),
            SarasvatiSerializationApiComponent(),
            SarasvatiUtilitiesApiComponent(),
            SarasvatiEventsApiComponent()
        ])

        self.__processor = self.plugins.get("processor").get()

    @property
    def plugins(self):
        return self.get_component(SarasvatiPluginsApiComponent.COMPONENT_NAME)

    @property
    def serialization(self):
        return self.get_component(SarasvatiSerializationApiComponent.COMPONENT_NAME)

    @property
    def utilities(self):
        return self.get_component(SarasvatiUtilitiesApiComponent.COMPONENT_NAME)

    @property
    def events(self):
        return self.get_component(SarasvatiEventsApiComponent.COMPONENT_NAME)

    @property
    def processor(self):
        return self.__processor

    def open_brain(self, path):
        logging.info("Opening brain from {}".format(path))
        storage_path = os.path.join(path, "db.json")
        storage_plugin = self.plugins.get("storage")
        storage = storage_plugin.open(storage_path)
        self.brain = Brain(storage)
        self.execute = self.brain.commands.execute
        return self.brain
