from yapsy.IPlugin import IPlugin as YapsyPlugin
from yapsy.PluginManager import PluginManager as YapsyPluginManager

from sarasvati import get_api


class PluginManager:
    __EXTENSION = "plugin"
    __CORE_PLUGINS_PATH = "plugins"

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
        :rtype: Type[Plugin]
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

    @staticmethod
    def __convert(obj):
        obj.plugin_object.info = PluginInfo(obj.name, obj.version, obj.path)
        return obj.plugin_object


class PluginInfo:
    def __init__(self, name, version, path, description=None):
        self.name = name
        self.version = version
        self.description = description
        self.path = path


class Plugin(YapsyPlugin):
    """
    Provides basic plugin interface
    """
    def __init__(self):
        super().__init__()
        self._api = get_api()
        self.info = None


class ApplicationPlugin(Plugin):
    pass


class StoragePlugin(Plugin):
    def open(self, path):
        """
        Opens storage
        :type path: str
        :rtype: Type[Storage]
        :param path: Path to open storage from
        """
        pass


class CommandsPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.__console_commands = {}

    def get_console_commands(self):
        return self.__console_commands

    def _register_console_command(self, name, handler):
        self.__console_commands[name] = handler


class ProcessorPlugin(Plugin):
    def get(self):
        pass


class ToolboxPlugin(Plugin):
    def get(self, engine):
        pass
