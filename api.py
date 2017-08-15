from optparse import OptionParser

from sarasvati.api import SarasvatiApi as GenericSarasvatiApi


class SarasvatiApi(GenericSarasvatiApi):
    def __init__(self):
        super().__init__()

        self.__parser = OptionParser()
        self.__parser.add_option("-a", "--app", action="store", type="string", dest="app_plugin", help="runs plugin")
        (self.__cmd_options, args) = self.__parser.parse_args()

    def get_application_plugin(self):
        plugin_name = self.__cmd_options.app_plugin or "GUI"
        plugins = self.plugins.find("application")
        filtered = filter(lambda x: x.info.name == plugin_name, plugins)
        result = list(filtered)
        return result[0] if len(result) > 0 else None
