from api.commands import Command
import colored
from colored import stylize


class ListCommand(Command):
    def __init__(self, api):
        super().__init__(api)
        self.__title_style = colored.fg("green")

    def execute(self):
        for thought in self._api.database.find(None) or []:
            print(
                stylize(thought.title, self.__title_style),
                thought.description)

    def revert(self):
        pass
