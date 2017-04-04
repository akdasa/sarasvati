class Processor:
    def __init__(self, plugins, api):
        """
        Initializes new instance of the Processor class.
        :param plugins: Array of CommandsPlugin
        :param api: Instance of CommandApi
        """
        self.__plugins = plugins
        self.__api = api
        self.__history = []

    def execute(self, line):
        """
        Executes specified query
        :param line: Command to execute
        """
        if line == "revert" and self.__history:
            c = self.__history.pop()
            self.__revert_command(c)
        self.__execute_line(line)

    @property
    def prompt(self):
        if self.__api.active_thought:
            return str(self.__api.active_thought.title) + "> "
        return "> "

    def __execute_line(self, line):
        command = self.__parse_line(line)
        if command:
            command.execute(self.__api)
            self.__history.append(command)

    def __parse_line(self, prompt):
        for plugin in self.__plugins:
            return plugin.parse(prompt, self.__api)

    def __revert_command(self, command):
        command.revert(self.__api)
