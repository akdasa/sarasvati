from api.plugins import CommandsPlugin
from .commands import CreateCommand, DeleteCommand


class GenericCommandsPlugin(CommandsPlugin):
    def get_commands(self):
        return [CreateCommand, DeleteCommand]

