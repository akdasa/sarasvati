from inspect import signature

from yapsy.IPlugin import IPlugin as YapsyPlugin
from yapsy.PluginManager import PluginManager as YapsyPluginManager


class PluginManager:
    __EXTENSION = "plugin"
    __CORE_PLUGINS_PATH = "sarasvati"

    def __init__(self, path="plugins", categories=None, api=None):
        """
        Initializes new instance of the PluginManager class
        :param path: path to the plugins, default: "plugins"
        :param categories: categories mappings
        """
        self.__path = [self.__CORE_PLUGINS_PATH, path]
        self.__categories = categories or []
        self.__api = api

        # Configure plugin manager
        self.__manager = YapsyPluginManager()
        self.__manager.getPluginLocator().setPluginInfoExtension(self.__EXTENSION)
        self.__manager.setPluginPlaces(self.__path)
        self.__manager.setCategoriesFilter(self.__categories)

        # Collect plugins
        self.__manager.collectPlugins()

    def find(self, category):
        """
        Returns list of plugins by specified category
        :param category: Category
        :return: Array of plugins
        """
        result = []
        for plugin in self.__manager.getPluginsOfCategory(category):
            result.append(self.__convert(plugin))
        return result

    def get(self, category):
        """
        Returns one plugin of category. Raises exception if none or more than one found
        :param category: Category
        :return: Plugin
        """
        plugins = self.find(category)
        count = len(plugins)
        if count == 1:
            return plugins[0]
        elif count == 0:
            raise Exception("No plugin found")
        elif count > 1:
            raise Exception("More than one plugin found")

    def __convert(self, obj):
        obj.plugin_object.api = self.__api
        obj.plugin_object.name = obj.name
        obj.plugin_object.version = obj.version
        return obj.plugin_object


class Plugin(YapsyPlugin):
    """
    Provides basic plugin interface
    """
    def __init__(self):
        super().__init__()
        self.api = None


class ApplicationPlugin(Plugin):
    pass


class StoragePlugin(Plugin):
    def add(self, thought):
        pass

    def update(self, thought):
        pass

    def delete(self, thought):
        pass

    def search(self, query):
        pass

    def get(self, query):
        pass


class CommandsPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.__console_commands = {}

    def get_console_commands(self):
        return self.__console_commands

    def _register_console_command(self, name, command_class, arguments_map=None):
        meta = {"class": command_class, "args_map": arguments_map}

        if not arguments_map:
            meta["args_cnt"] = len(signature(command_class.__init__).parameters) - 2  # (self, api)

        self.__console_commands[name] = meta
