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


class ShowCommand(Command):
    def __init__(self, api, thought):
        super().__init__(api)
        self.__title_style = colored.fg("green") + colored.attr("bold")
        self.__link_style = colored.fg("blue") + colored.attr("underlined")
        self.__thought = thought

    def execute(self):
        print(stylize(self.__thought.title, self.__title_style))
        print(self.__thought.description)

        for thought in self.__thought.links.all:
            print("Link:", stylize(thought.title, self.__link_style))

    def revert(self):
        pass
