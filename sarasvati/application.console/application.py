from api.commands import CommandApi


class SarasvatiConsoleApplication:
    __QUIT_COMMAND = "quit"

    def __init__(self, database_plugin, command_plugins):
        self.__command_plugins = command_plugins
        self.__command_api = CommandApi(database_plugin)

    def run(self):
        query = None
        while query != self.__QUIT_COMMAND:
            query = input(self.__prompt())
            self.__execute_commands(query, self.__command_plugins)

    def __execute_commands(self, prompt, plugins):
        for plugin in plugins:
            command = plugin.parse(prompt, self.__command_api)
            if command:
                command.execute(self.__command_api)
            else:
                print("Unknown command")

    def __prompt(self):
        if self.__command_api.active_thought:
            return str(self.__command_api.active_thought.title) + "> "
        return "> "
