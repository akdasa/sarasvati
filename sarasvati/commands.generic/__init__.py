from api.plugins import CommandsPlugin
from .commands import CreateCommand, DeleteCommand, SetTitleCommand, ActivateThoughtCommand, SetDescriptionCommand


class GenericCommandsPlugin(CommandsPlugin):
    def parse(self, prompt, api):
        tokens = prompt.split(" ")
        command_name = tokens[0]

        if command_name == "title":
            return SetTitleCommand(api.active_thought, tokens[1])
        if command_name == "description":
            return SetDescriptionCommand(api.active_thought, tokens[1])
        elif command_name == "create":
            return CreateCommand(tokens[1])
        elif command_name == "delete":
            thought = api.database.find(tokens[1])
            return DeleteCommand(thought)
        elif command_name == "activate":
            thought = api.database.find(tokens[1])
            return ActivateThoughtCommand(thought)
