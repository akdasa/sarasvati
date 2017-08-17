import logging
import os

from sarasvati import set_api
from sarasvati.api.commands import SarasvatiCommandsApiComponent
from sarasvati.api.events import SarasvatiEventsApiComponent
from sarasvati.api.plugins import SarasvatiPluginsApiComponent
from sarasvati.api.serialization import SarasvatiSerializationApiComponent
from sarasvati.api.utilities import SarasvatiUtilitiesApiComponent
from sarasvati.brain import Brain
from sarasvati.models import Composite


class SarasvatiApi(Composite):
    """
    Sarasvati application programming interface
    """
    def __init__(self):
        set_api(self)
        super().__init__()

        self.brain = None
        self.storage = None

        self.add_components([
            SarasvatiPluginsApiComponent(),
            SarasvatiSerializationApiComponent(),
            SarasvatiUtilitiesApiComponent(),
            SarasvatiEventsApiComponent(),
            SarasvatiCommandsApiComponent()
        ])

    @property
    def plugins(self):
        """
        Returns plugin component
        :rtype: SarasvatiPluginsApiComponent
        :return: Plugins component
        """
        return self.get_component(SarasvatiPluginsApiComponent.COMPONENT_NAME)

    @property
    def serialization(self):
        """
        Returns serialization component
        :rtype: SarasvatiSerializationApiComponent
        :return: Serialization component
        """
        return self.get_component(SarasvatiSerializationApiComponent.COMPONENT_NAME)

    @property
    def utilities(self):
        """
        Returns utilities component
        :rtype: SarasvatiUtilitiesApiComponent
        :return: Utilities component
        """
        return self.get_component(SarasvatiUtilitiesApiComponent.COMPONENT_NAME)

    @property
    def events(self):
        """
        Returns events component
        :rtype: SarasvatiEventsApiComponent
        :return: Events component
        """
        return self.get_component(SarasvatiEventsApiComponent.COMPONENT_NAME)

    @property
    def commands(self):
        """
        Returns commands component
        :rtype: SarasvatiCommandsApiComponent
        :return: Commands component
        """
        return self.get_component(SarasvatiCommandsApiComponent.COMPONENT_NAME)

    def execute(self, command, transaction=None):
        """
        Executes command
        :param command: String or Command instance
        :param transaction: Transaction
        :return: Command execution result
        """
        return self.commands.execute(command, transaction)

    def open_brain(self, path):
        """
        Opens brain from specified path
        :rtype: Brain
        :param path: Path to oben brain from
        :return: Brain
        """
        logging.info("Opening brain from {}".format(path))
        storage_path = os.path.join(path, "db.json")
        storage_plugin = self.plugins.get("storage")
        self.storage = storage_plugin.open(storage_path)
        self.brain = Brain(self.storage)
        return self.brain
