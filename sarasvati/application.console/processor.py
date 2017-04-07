import shlex


class Processor:
    def __init__(self, commands, api):
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
        if line == "revert" and self.__history:
            c = self.__history.pop()
            c.revert()
        elif line == "quit":
            pass
        else:
            self.__execute_line(line)

    @property
    def prompt(self):
        if self.__api.active_thought:
            return str(self.__api.active_thought.title) + "> "
        return "> "

    def __execute_line(self, line):
        try:
            command = self.__parse_line(line)
            command.execute()
            self.__history.append(command)
        except Exception as e:
            print(e)

    def __parse_line(self, prompt):
        tokens = shlex.split(prompt)
        token_args = tokens[1:]
        token_cmd = tokens[0]
        meta = self.__commands.get(token_cmd)

        if meta:
            cmd_args_cnt = meta.get("args_cnt", None)
            cmd_args_map = meta.get("args_map", None)
            cmd_class = meta["class"]

            if not cmd_args_map:
                if len(token_args) != cmd_args_cnt:
                    raise Exception("'{}' takes {} arguments but {} were given".format(token_cmd, cmd_args_cnt, len(token_args)))

            cmd_args = cmd_args_map(self.__api, token_args) if cmd_args_map else token_args
            return cmd_class(self.__api, *cmd_args)
        else:
            raise Exception("Unknown command '{}'".format(token_cmd))
