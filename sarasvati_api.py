from api.plugins import ApplicationPlugin, DatabasePlugin, PluginManager, CommandsPlugin


class SarasvatiApi:
    def __init__(self):
        # Load and activate one of the application plugin
        self.plugins = PluginManager(
            categories={
                "application": ApplicationPlugin,
                "database": DatabasePlugin,
                "commands": CommandsPlugin
            }, api=self)
