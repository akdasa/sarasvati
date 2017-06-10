from sarasvati.plugins import CommandsPlugin
from .handlers import *


class ShellCommandsPlugin(CommandsPlugin):
    def __init__(self):
        super().__init__()
        self._register_console_command("/q", quit_)

        self._register_console_command("/ls", ls)
        self._register_console_command("/show", show)
        self._register_console_command("/quit", quit_)
