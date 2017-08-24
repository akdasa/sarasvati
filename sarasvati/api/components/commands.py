from sarasvati.models import Component


class SarasvatiCommandsApiComponent(Component):
    COMPONENT_NAME = "commands"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__processor = None
        self.__composite = None

    def execute(self, command, transaction=None):
        if isinstance(command, str):
            return self.__processor.execute(command)
        else:
            return self.__composite.brain.commands.execute(command, transaction)

    def on_added(self, composite):
        self.__processor = composite.plugins.get("processor").get()
        self.__composite = composite
