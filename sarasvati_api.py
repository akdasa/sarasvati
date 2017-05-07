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


class SarasvatiApiEvents:
    def __init__(self):
        self.thoughtCreated = Event()
        self.thoughtSelected = Event()
        self.thoughtChanging = Event()
        self.thoughtChanged = Event()
