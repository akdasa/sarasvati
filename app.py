from sarasvati_api import SarasvatiApi

# Sarasvati Application info
version = "0.0.1 Born"
print("Sarasvati " + version)

# Get one application plugin and activate it
api = SarasvatiApi()
application = api.plugins.get("application")
application.activate()
application.deactivate()
