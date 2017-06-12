from sarasvati.brain.model import Component
from sarasvati.plugins import *


class SarasvatiPluginsApiComponent(Component):
    COMPONENT_NAME = "plugins"

    def __init__(self):
        super().__init__(self.COMPONENT_NAME)
        self.__plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "storage": StoragePlugin,
                "commands": CommandsPlugin,
                "processor": ProcessorPlugin
            })

    def find(self, category):
        return self.__plugins.find(category)

    def get(self, category):
        return self.__plugins.get(category)
