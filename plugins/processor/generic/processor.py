from pycopa import parse

from sarasvati.exceptions import CommandException


class Processor:
    def __init__(self, api, commands):
        """
        Initializes new instance of the Processor class.
        :param api: Instance to pass to handlers
        :param commands: Dictionary of commands meta
        """
        self.__api = api
        self.__commands = commands

    def execute(self, line):
        """
        Executes specified query
        :param line: Command to execute
        """
        args = parse(line)
        command = args.get("command")
        handler = self.__get_handler(command)
        return handler(self.__api, args)

    def __get_handler(self, command):
        handler = self.__commands.get(command)
        if not handler:
            raise CommandException("Unknown command '{}'".format(command))
        return handler

