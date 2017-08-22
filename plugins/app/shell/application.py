import colored
from colored import stylize
from pycopa.exception import PycopaException

from sarasvati.application import SarasvatiApplication
from sarasvati.commands import CommandException, CommandResult
from .prompt import get_prompt


class SarasvatiConsoleApplication(SarasvatiApplication):
    __QUIT_COMMANDS = ["/quit", "/q"]
    __ERROR_STYLE = colored.fg("red")
    __OK_STYLE = colored.fg("blue")

    def __init__(self):
        super().__init__()

    def run(self):
        query = None
        while query not in self.__QUIT_COMMANDS:
            query = get_prompt(self.__prompt_state())
            result = self.__execute(query)
            self.__print_result(result)

    def __execute(self, query):
        try:
            return self._api.execute(query)
        except CommandException as e:
            print(stylize(e, self.__ERROR_STYLE))
        except PycopaException as e:
            print(stylize("Syntax error: " + str(e), self.__ERROR_STYLE))

    def __prompt_state(self):
        thought = self._brain.state.active_thought
        if thought:
            return thought.title + "> "
        return "> "

    def __print_result(self, result):
        if not isinstance(result, CommandResult):
            return

        if result.message:
            print(stylize(result.message, self.__OK_STYLE))
