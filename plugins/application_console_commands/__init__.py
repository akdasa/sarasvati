from sarasvati.plugins import CommandsPlugin
from .commands import *
from ._maps import *


class ApplicationConsoleCommandsPlugin(CommandsPlugin):
    def __init__(self):
        super().__init__()
        self._register_console_command("ls", ListCommand)
        self._register_console_command("show", ShowCommand, show_command_map)
