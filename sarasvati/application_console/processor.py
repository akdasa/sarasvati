import shlex


class Processor:
    __REVERT_COMMAND = "revert"
    __QUIT_COMMAND = "quit"

    def __init__(self, api, commands):
        """
        Initializes new instance of the Processor class.
        :param commands: Dictionary of commands meta
        :param api: Instance of CommandApi
        """
        self.__api = api
        self.__commands = commands.copy()
        self.__history = []

    def execute(self, line):
        """
        Executes specified query
        :param line: Command to execute
        """
        if line == self.__REVERT_COMMAND and self.__history:
            c = self.__history.pop()
            c.revert()
        elif line != self.__QUIT_COMMAND:
            self.__execute_line(line)

    @property
    def prompt(self):
        active_thought = self.__api.active_thought
        if active_thought:
            return str(active_thought.title) + "> "
        return "> "

    def __execute_line(self, line):
        try:
            command = self.__parse(line)
            command.execute()
            self.__history.append(command)
        except Exception as e:
            print(e)
            raise

    def __parse(self, line):
        tokens = shlex.split(line)
        token_args = tokens[1:]
        token_cmd = tokens[0]
        meta = self.__commands.get(token_cmd)

        if meta:
            cmd_args_cnt = meta.arguments_count
            cmd_args_map = meta.arguments_map
            cmd_class = meta.command_class

            if not cmd_args_map:
                if len(token_args) != cmd_args_cnt:
                    raise Exception(
                        "'{}' takes {} arguments but {} were given".format(token_cmd, cmd_args_cnt, len(token_args)))

            cmd_args = cmd_args_map(self.__api, token_args) if cmd_args_map else token_args
            return cmd_class(self.__api, *cmd_args)
        else:
            raise Exception("Unknown command '{}'".format(token_cmd))
