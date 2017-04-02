from api.commands import CommandApi
from .processor import Processor
from .commands import QuitCommand


class SarasvatiConsoleApplication:
    __QUIT_COMMAND = "quit"

    def __init__(self, database_plugin, command_plugins):
        self.__command_plugins = command_plugins
        self.__command_api = CommandApi(database_plugin)
        self.__processor = Processor(api=self.__command_api)

    def run(self):
        self.__load_commands(self.__command_plugins)
        self.__processor.register(QuitCommand)

        query = None
        while query != self.__QUIT_COMMAND:
            query = input(self.__processor.prompt())
            self.__processor.execute(query)

    def __load_commands(self, plugins):
        for plugin in plugins:
            plugins = plugin.get_commands() or []
            for command in plugins:
                self.__processor.register(command)
