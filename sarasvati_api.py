from api.commands import CommandException
from api.instance import set_api
from api.event import Event
from api.plugins import ApplicationPlugin, StoragePlugin, PluginManager, CommandsPlugin, SectionPlugin, ToolboxPlugin


class SarasvatiApi:
    def __init__(self):
        set_api(self)
        self.__events = SarasvatiApiEvents()
        self.__actions = SarasvatiApiActions(self)
        self.__plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "storage": StoragePlugin,
                "commands": CommandsPlugin,
                "section": SectionPlugin,
                "toolbox": ToolboxPlugin
            })

    @property
    def plugins(self):
        return self.__plugins

    @property
    def events(self):
        return self.__events

    @property
    def actions(self):
        return self.__actions

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


class SarasvatiApiActions:
    def __init__(self, api):
        self.__api = api

    def create_thought(self, title):
        thought = self.__api.brain.create_thought(title)
        self.__api.events.thoughtCreated.notify(thought)
        return thought

    def create_linked_thought(self, root, kind, title):
        thought = self.__api.brain.create_linked_thought(root, kind, title)
        self.__api.events.thoughtCreated.notify(thought)
        return thought

    def update_thought(self, thought):
        self.__api.brain.storage.update(thought)
        self.__api.events.thoughtChanged.notify(thought)