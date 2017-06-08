from sarasvati_api import SarasvatiApi
import logging

# Logging configuration
logging.basicConfig(filename='sarasvati.log',level=logging.DEBUG)

# Sarasvati Application info
version = "0.0.1 Born"
logging.info("Sarasvati " + version)

# Get one application plugin and activate it
api = SarasvatiApi()
application = api.get_application_plugin()

# Run application
if application is not None:
    application.activate()
    application.deactivate()
else:
    logging.critical("No specified application plugin found")
    print("No specified application plugin found")
