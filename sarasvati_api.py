from api.plugins import ApplicationPlugin, StoragePlugin, PluginManager, CommandsPlugin


class SarasvatiApi:
    def __init__(self):
        # Load and activate one of the application plugin
        self.plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "storage": StoragePlugin,
                "commands": CommandsPlugin
            }, api=self)
