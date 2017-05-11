from api.commands import CommandException
from api.instance import set_api
from api.event import Event
from api.plugins import ApplicationPlugin, StoragePlugin, PluginManager, CommandsPlugin, SectionPlugin


class SarasvatiApi:
    def __init__(self):
        set_api(self)
        self.__events = SarasvatiApiEvents()
        self.__plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "storage": StoragePlugin,
                "commands": CommandsPlugin,
                "section": SectionPlugin
            })

    @property
    def plugins(self):
        return self.__plugins

    @property
    def events(self):
        return self.__events

    @staticmethod
    def get_one(lst):
        """Returns one element from list, otherwise raises exception"""
        lst_len = len(lst)
        if lst_len == 0:
            raise CommandException("Nothing found")
        elif lst_len > 1:
            raise CommandException("More than one entity found")
        else:
            return lst[0]


class SarasvatiApiEvents:
    def __init__(self):
        self.thoughtCreated = Event()
        self.thoughtSelected = Event()
        self.thoughtChanging = Event()
        self.thoughtChanged = Event()
