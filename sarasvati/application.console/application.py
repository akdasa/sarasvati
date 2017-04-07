from api.commands import CommandApi
from .processor import Processor


class SarasvatiConsoleApplication:
    __QUIT_COMMAND = "quit"

    def __init__(self, database_plugin, command_plugins):
        """
        Initializes new instance of the SarasvatiConsoleApplication class.
        :type command_plugins: [CommandsPlugin]
        :type database_plugin: DatabasePlugin
        :param database_plugin: Database 
        :param command_plugins: Commands
        """
        command_api = CommandApi(database_plugin)
        commands = self.__collect_commands(command_plugins)
        self.__processor = Processor(commands, command_api)

    def run(self):
        """
        Starts application
        """
        query = None
        while query != self.__QUIT_COMMAND:
            query = input(self.__processor.prompt)
            self.__processor.execute(query)

    @staticmethod
    def __collect_commands(command_plugins):
        result = {}
        for plugin in command_plugins:
            result.update(plugin.get_console_commands())
        return result
