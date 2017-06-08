from sarasvati.commands import Command
import colored
from colored import stylize


class ListCommand(Command):
    def __init__(self, title):
        super().__init__()
        self.__title = title
        self.__title_style = colored.fg("green")

    def execute(self):
        search_result = self._api.brain.search.by_title(self.__title, operator="~~")
        for thought in search_result:
            print(stylize(thought.title, self.__title_style), thought.description)

    def revert(self):
        pass


class ShowCommand(Command):
    def __init__(self, thought):
        super().__init__()
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
