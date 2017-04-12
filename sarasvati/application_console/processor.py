import shlex

from api.plugins import CommandException


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
            if command:
                command.execute()
                self.__history.append(command)
        except CommandException as e:
            print(e)

    def __parse(self, line):
        tokens = shlex.split(line)
        if len(tokens) <= 0:
            return None

        token_args = tokens[1:]
        token_cmd = tokens[0]
        meta = self.__commands.get(token_cmd)

        if not meta:
            raise CommandException("Unknown command '{}'".format(token_cmd))

        args_cnt = meta.arguments_count
        args_map = meta.arguments_map
        cmd_class = meta.command_class
        if not args_map and len(token_args) != args_cnt:
            raise CommandException("'{}' takes {} arguments but {} were given"
                                   .format(token_cmd, args_cnt, len(token_args)))

        cmd_args = args_map(self.__api, token_args) if args_map else token_args
        return cmd_class(self.__api, *cmd_args)

