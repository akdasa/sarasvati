from api.commands import CommandApi
from .processor import Processor


class SarasvatiConsoleApplication:
    __QUIT_COMMAND = "quit"

    def __init__(self, storage_plugin, command_plugins):
        """
        Initializes new instance of the SarasvatiConsoleApplication class.
        :type command_plugins: [CommandsPlugin]
        :type storage_plugin: DatabasePlugin
        :param storage_plugin: Database 
        :param command_plugins: Commands
        """
        storage = storage_plugin.get_storage()
        command_api = CommandApi(storage)
        commands = self.__collect_commands(command_plugins)
        self.__processor = Processor(command_api, commands)

    def run(self):
        """
        Starts application
        """
        query = None
        while not self.__is_quit_command(query):
            prompt = self.__processor.prompt
            query = input(prompt)
            self.__processor.execute(query)

    def __is_quit_command(self, query):
        return query == self.__QUIT_COMMAND

    @staticmethod
    def __collect_commands(command_plugins):
        result = {}
        for plugin in command_plugins:
            commands = plugin.get_console_commands()
            result.update(commands)
        return result