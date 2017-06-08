from sarasvati import get_api
from sarasvati.commands import CommandException
from .parser import Parser


class Processor:
    __REVERT_COMMAND = "revert"
    __QUIT_COMMAND = "quit"

    def __init__(self, brain, commands):
        """
        Initializes new instance of the Processor class.
        :param commands: Dictionary of commands meta
        :param brain: Brain to manipulate with
        """
        self.__brain = brain
        self.__api = get_api()
        self.__parser = Parser(self.__api, commands)

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
        active_thought = self.__api.brain.state.active_thought
        if active_thought:
            return str(active_thought.title) + "> "
        return "> "

    def __execute_line(self, line):
        try:
            command = self.__parser.parse(line)
            if command:
                self.__brain.commands.execute(command)
        except CommandException as e:
            print(e)


