from logging import error

from pycopa import parse

from sarasvati import get_api
from sarasvati.commands import CommandException


class Processor:
    def __init__(self, commands):
        """
        Initializes new instance of the Processor class.
        :param commands: Dictionary of commands meta
        """
        self.__commands = commands
        self.__api = get_api()

    def execute(self, line):
        """
        Executes specified query
        :param line: Command to execute
        """
        try:
            args = parse(line)
            command = args.get("command")
            handler = self.__get_handler(command)
            result = handler(self.__api, args)
            self.__print_result(result)
        except CommandException as e:
            error(e)
            print(e)

    def __get_handler(self, command):
        handler = self.__commands.get(command)
        if not handler:
            raise CommandException("Unknown command '{}'".format(command))
        return handler

    @staticmethod
    def __print_result(result):
        if not result:
            return
        if isinstance(result, list):
            for e in result:
                print(e)
        else:
            print(result)
