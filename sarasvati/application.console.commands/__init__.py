from api.plugins import CommandsPlugin
from .commands import ListCommand


class ApplicationConsoleCommandsPlugin(CommandsPlugin):
    def parse(self, prompt, api):
        tokens = prompt.split(" ")
        command_name = tokens[0]

        if command_name == "ls":
            return ListCommand()
