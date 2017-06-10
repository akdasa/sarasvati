from logging import error

from sarasvati import get_api
from sarasvati.commands import CommandException
from .parser import Parser


class Processor:
    __REVERT_COMMAND = "revert"
    __QUIT_COMMAND = "quit"

    def __init__(self, brain, commands, state=None):
        """
        Initializes new instance of the Processor class.
        :param commands: Dictionary of commands meta
        :param brain: Brain to manipulate with
        """
        self.__brain = brain # удалить. используется только для отката команд
        self.__parser = Parser(commands)
        self.__state = state
        self.__api = get_api()

    def execute(self, line):
        """
        Executes specified query
        :param line: Command to execute
        """
        if line == self.__REVERT_COMMAND:
            self.__brain.commands.revert()
        elif line != self.__QUIT_COMMAND:
            self.__execute_line(line)

    @property
    def prompt(self):
        if self.__state:
            return str(self.__state()) + "> "
        return "> "

    def __execute_line(self, line):
        try:
            handler, args = self.__parser.parse(line)
            if not handler:
                return

            result = handler(self.__api, args)
            if result:
                if isinstance(result, list):
                    for e in result:
                        print(e)
                else:
                    print(result)
        except CommandException as e:
            error(e)
            print(e)
