from api.application import SarasvatiApplication
from api.brain import Brain
from prompt_toolkit import prompt as ptprompt
from prompt_toolkit.history import InMemoryHistory
from .processor import Processor


class SarasvatiConsoleApplication(SarasvatiApplication):
    __QUIT_COMMAND = "quit"

    def __init__(self, storage_plugin, command_plugins):
        """
        Initializes new instance of the SarasvatiConsoleApplication class.
        :type command_plugins: [CommandsPlugin]
        :type storage_plugin: StoragePlugin
        :param storage_plugin: Storage 
        :param command_plugins: Commands
        """
        super().__init__()
        storage = storage_plugin.get_storage()
        commands = self.__collect_commands(command_plugins)
        self.__brain = Brain(storage)
        self.__processor = Processor(self.__brain, commands)
        self._api.brain = self.__brain

    def run(self):
        """
        Starts application
        """
        history = InMemoryHistory()
        query = None
        while not self.__is_quit_command(query):
            prompt = self.__processor.prompt
            query = ptprompt(prompt, history=history)
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
