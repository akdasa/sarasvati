from sarasvati.plugins import ProcessorPlugin
from .processor import Processor


class GenericProcessorPlugin(ProcessorPlugin):
    def __init__(self):
        super().__init__()

    def get(self):
        commands = {}
        command_plugins = self._api.plugins.find("commands")
        for plugin in command_plugins:
            c = plugin.get_console_commands()
            commands.update(c)
        return Processor(self._api, commands)
