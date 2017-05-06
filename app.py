import sys
from sarasvati_api import SarasvatiApi


def get_application_plugin(plugin_name):
    plugins = api.plugins.find("application")
    filtered = filter(lambda x: x.name == plugin_name, plugins)
    result = list(filtered)
    return result[0] if len(result) > 0 else None


def get_application_plugin_name():
    return sys.argv[1] if len(sys.argv) > 1 else "Application.Gui"


# Sarasvati Application info
version = "0.0.1 Born"
print("Sarasvati " + version)

# Get one application plugin and activate it
api = SarasvatiApi()
apn = get_application_plugin_name()
application = get_application_plugin(apn)


if application is not None:
    application.activate()
    application.deactivate()
else:
    print("No specified application plugin found")