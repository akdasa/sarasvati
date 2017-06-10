from pycopa import parse

from sarasvati.commands import CommandException


class Parser:
    def __init__(self, commands):
        self.__commands = commands  # поднять уровнем выше в __execute_line

    def parse(self, line):
        result = parse(line)
        command = result["command"]
        handler = self.__commands.get(command)

        if not handler:
            raise CommandException("Unknown command '{}'".format(command))

        return handler, result
