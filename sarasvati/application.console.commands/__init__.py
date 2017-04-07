from api.plugins import CommandsPlugin
from .commands import ListCommand


class ApplicationConsoleCommandsPlugin(CommandsPlugin):
    def __init__(self):
        super().__init__()
        self._register_console_command("ls", ListCommand)
