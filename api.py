import os

import logging

from sarasvati.brain import Brain
from sarasvati.brain.model import IdentityComponent
from sarasvati.brain.thought import DefinitionComponent, LinksComponent, Thought
from sarasvati.commands import CommandException
from sarasvati import set_api
from sarasvati.event import Event
from sarasvati.plugins import *
from optparse import OptionParser


class SarasvatiApi:
    def __init__(self):
        set_api(self)

        self.brain = None
        self.execute = None
        self.__events = SarasvatiApiEvents()
        # self.__actions = SarasvatiApiActions(self)
        self.__serialization = SarasvatiApiSerialization()
        self.__plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "storage": StoragePlugin,
                "commands": CommandsPlugin,
                "processor": ProcessorPlugin
            })
        self.__parser = OptionParser()
        self.__parser.add_option("-a", "--app", action="store", type="string", dest="app_plugin", help="runs plugin")
        (self.__cmd_options, args) = self.__parser.parse_args()

    def find_one_by_title(self, title, arg_name):
        _n = "No thought found for '{}' argument".format(arg_name)
        _m = "Multiple thoughts found for '{}' argument".format(arg_name)
        search = self.brain.search.by_title(title)
        return self.get_one(search, _n, _m)

    def open_brain(self, path):
        logging.info("Opening brain from {}".format(path))
        storage_path = os.path.join(path, "db.json")
        storage_plugin = self.__plugins.get("storage")
        storage = storage_plugin.open(storage_path)
        self.brain = Brain(storage)
        self.execute = self.brain.commands.execute
        return self.brain

    @property
    def plugins(self):
        return self.__plugins

    @property
    def events(self):
        return self.__events

    # @property
    # def actions(self):
    #     return self.__actions

    @property
    def serialization(self):
        return self.__serialization

    @staticmethod
    def get_one(lst, nothing_err="Nothing found", more_err="More than one entity found"):
        """Returns one element from list, otherwise raises exception"""
        lst_len = len(lst)
        if lst_len == 0:
            raise CommandException(nothing_err)
        elif lst_len > 1:
            raise CommandException(more_err)
        else:
            return lst[0]

    def get_application_plugin(self):
        plugin_name = self.__cmd_options.app_plugin or "Shell"
        plugins = self.__plugins.find("application")
        filtered = filter(lambda x: x.info.name == plugin_name, plugins)
        result = list(filtered)
        return result[0] if len(result) > 0 else None


class SarasvatiApiEvents:
    def __init__(self):
        self.thoughtCreated = Event()
        self.thoughtSelected = Event()
        self.thoughtChanging = Event()
        self.thoughtChanged = Event()


# class SarasvatiApiActions:
#     def __init__(self, api):
#         self.__api = api
#
#     def create_thought(self, title):
#         command = CreateCommand(title)
#         thought = self.__api.brain.commands.execute(command)
#         self.__api.events.thoughtCreated.notify(thought)
#         return thought
#
#     def create_linked_thought(self, root, kind, title):
#         ex = self.__api.brain.commands.execute
#         thought = ex(CreateCommand(title))
#         ex(LinkCommand(root, thought, "child"))
#         ex(LinkCommand(thought, root, "parent"))
#
#         self.__api.events.thoughtCreated.notify(thought)
#         return thought
#
#     def updating_thought(self, thought):
#         self.__api.events.thoughtChanging.notify(thought)
#
#     def update_thought(self, thought):
#         self.__api.brain.storage.update(thought)
#         self.__api.events.thoughtChanged.notify(thought)


class SarasvatiApiSerialization:
    def __init__(self):
        pass

    def get_options(self, storage):
        return {
            "get_component": self.__get_component,
            "get_linked": self.__get_linked(storage)}

    @staticmethod
    # TODO: set serialization map
    def __get_component(key):
        options = {
            IdentityComponent.COMPONENT_NAME: IdentityComponent,
            DefinitionComponent.COMPONENT_NAME: DefinitionComponent,
            LinksComponent.COMPONENT_NAME: LinksComponent}
        res = options.get(key, None)
        if res:
            return res()
        return None

    @staticmethod
    def __get_linked(storage):
        def result(key):
            cached = storage.cache.get(key)
            if not cached:
                thought = Thought("<LAZY>", key=key)
                storage.cache.add(thought, lazy=True)
                return thought
            else:
                return cached
        return result
