from api.plugins import CommandsPlugin
from .commands import *
from ._maps import *


class GenericCommandsPlugin(CommandsPlugin):
    def __init__(self):
        super().__init__()
        self._register_console_command("create", CreateCommand)
        self._register_console_command("delete", DeleteCommand, delete_map)
        self._register_console_command("activate", ActivateCommand, activate_map)
        self._register_console_command("title", SetTitleCommand, set_title_or_description_map)
        self._register_console_command("description", SetDescriptionCommand, set_title_or_description_map)
