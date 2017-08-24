import logging

from sarasvati import set_api
from sarasvati.api.components import *
from sarasvati.brain import Brain
from sarasvati.models import Composite
from sarasvati.serialization import *


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
        :param path: Path to open brain from
        :return: Brain
        """
        logging.info("Opening brain from {}".format(path))
        storage_plugin = self.plugins.get("storage")
        self.storage = storage_plugin.open(path)

        self.storage.serializer.register("identity", IdentityComponentSerializer())
        self.storage.serializer.register("definition", DefinitionComponentSerializer())
        self.storage.serializer.register("links", LinksComponentSerializer(self.storage))

        self.brain = Brain(self.storage)
        return self.brain
