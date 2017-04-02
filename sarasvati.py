from api.plugins import ApplicationPlugin
from api.plugin_manager import PluginManager

# Sarasvati Application info
version = "0.0.1 Born"
print("Sarasvati " + version)

# Load and activate one of the application plugin
plugins = PluginManager(categories={"application": ApplicationPlugin})
applications = plugins.get("application")
count = len(applications)

if count == 1:
    applications[0].activate()
elif count == 0:
    print("No application plugin found")
elif count > 1:
    print("More than one application plugin found")
