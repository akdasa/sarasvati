from inspect import signature

from yapsy.IPlugin import IPlugin as YapsyPlugin
from yapsy.PluginManager import PluginManager as YapsyPluginManager


class PluginManager:
    __EXTENSION = "plugin"
    __CORE_PLUGINS_PATH = "sarasvati"

    def __init__(self, path="plugins", categories=None):
        """
        Initializes new instance of the PluginManager class
        :param path: path to the plugins, default: "plugins"
        :param categories: categories mappings
        """
        self.__path = [self.__CORE_PLUGINS_PATH, path]
        self.__categories = categories or {}

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
        obj.plugin_object.info = PluginInfo(obj.name, obj.version)
        return obj.plugin_object


class PluginInfo:
    def __init__(self, name, version, description=None):
        self.name = name
        self.version = version
        self.description = description


class Plugin(YapsyPlugin):
    """
    Provides basic plugin interface
    """
    def __init__(self):
        super().__init__()


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
        init_params_count = len(signature(command_class.__init__).parameters)
        arguments_count = None if arguments_map else init_params_count - 2
        self.__console_commands[name] = CommandMeta(name, command_class, arguments_map, arguments_count)


class CommandMeta:
    def __init__(self, name, command_class, arguments_map=None, arguments_count=None):
        self.__name = name
        self.__command_class = command_class
        self.__arguments_map = arguments_map
        self.__arguments_count = arguments_count

    @property
    def name(self):
        return self.__name

    @property
    def command_class(self):
        return self.__command_class

    @property
    def arguments_map(self):
        return self.__arguments_map

    @property
    def arguments_count(self):
        return self.__arguments_count


class SectionPlugin(Plugin):
    def get_widget(self):
        pass

    def get_section_name(self):
        pass
