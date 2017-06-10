from sarasvati.application import SarasvatiApplication
from sarasvati.brain import Brain
from .processor import Processor
from .prompt import get_prompt


class SarasvatiConsoleApplication(SarasvatiApplication):
    __QUIT_COMMANDS = ["/quit", "/q"]

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
        self.__processor = Processor(commands)
        self._api.brain = self.__brain  # todo: ugly

    def run(self):
        """
        Starts application
        """
        query = None
        while not self.__is_quit_command(query):
            query = get_prompt(self.__prompt_state())
            self.__processor.execute(query)

    def __is_quit_command(self, query):
        return query in self.__QUIT_COMMANDS

    @staticmethod
    def __collect_commands(command_plugins):
        result = {}
        for plugin in command_plugins:
            commands = plugin.get_console_commands()
            result.update(commands)
        return result

    def __prompt_state(self):
        thought = self.__brain.state.active_thought
        if thought:
            return thought.title + "> "
        return "> "
