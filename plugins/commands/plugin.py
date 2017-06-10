from sarasvati.plugins import CommandsPlugin
from .handlers import *


class GenericCommandsPlugin(CommandsPlugin):
    def __init__(self):
        super().__init__()
        self._register_console_command("/a", activate)
        self._register_console_command("/c", create)
        self._register_console_command("/d", delete)
        self._register_console_command("/u", update)
        self._register_console_command("/l", link)
        self._register_console_command("/r", revert)

        self._register_console_command("/activate", activate)
        self._register_console_command("/create", create)
        self._register_console_command("/delete", delete)
        self._register_console_command("/update", update)
        self._register_console_command("/link", link)
        self._register_console_command("/revert", revert)
