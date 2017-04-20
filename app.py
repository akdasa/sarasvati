import sys

from sarasvati_api import SarasvatiApi

# Sarasvati Application info
version = "0.0.1 Born"
print("Sarasvati " + version)

# Get one application plugin and activate it
api = SarasvatiApi()
applications = api.plugins.find("application")
application = None

if len(applications) == 1:
    application = applications[0]
elif len(applications) > 1:
    application = applications[1]  # todo: specify by command line
else:
    print("More than one 'application' plugin found")

if application is not None:
    application.activate()
    application.deactivate()