import shlex

from api.plugins import CommandException


class Parser:
    def __init__(self, api, commands):
        self.__commands = commands
        self.__api = api

    def parse(self, line):
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