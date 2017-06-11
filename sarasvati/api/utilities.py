from sarasvati.brain.model import Component
from sarasvati.commands import CommandException


class SarasvatiUtilitiesApiComponent(Component):
    COMPONENT_NAME = "utilities"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__composite = None

    def on_added(self, composite):
        self.__composite = composite

    def find_one_by_title(self, title, arg_name=None):
        brain = self.__composite.brain

        if not arg_name:
            _n = "No thought '{}' found".format(title)
            _m = "Multiple thoughts found"
        else:
            _n = "No thought '{}' found for '{}' argument".format(title, arg_name)
            _m = "Multiple thoughts found for '{}' argument".format(arg_name)
        search = brain.search.by_title(title)

        lst_len = len(search)
        if lst_len == 0:
            raise CommandException(_n)
        elif lst_len > 1:
            raise CommandException(_m)
        else:
            return search[0]
