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
        self.__categories = categories or []

        # Configure plugin manager
        self.__manager = YapsyPluginManager()
        self.__manager.getPluginLocator().setPluginInfoExtension(self.__EXTENSION)
        self.__manager.setPluginPlaces(self.__path)
        self.__manager.setCategoriesFilter(self.__categories)

        # Collect plugins
        self.__manager.collectPlugins()

    def get(self, category):
        """
        Returns list of plugins by specified category
        :param category: Category
        :return: Array of plugins
        """
        result = []
        for plugin in self.__manager.getPluginsOfCategory(category):
            result.append(plugin.plugin_object)
        return result
