from api.plugins import ApplicationPlugin, StoragePlugin, PluginManager, CommandsPlugin, SectionPlugin


class SarasvatiApi:
    def __init__(self):
        # Load and activate one of the application plugin
        self.__plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "storage": StoragePlugin,
                "commands": CommandsPlugin,
                "section": SectionPlugin
            }, api=self)

    @property
    def plugins(self):
        return self.__plugins
