import os

from PyQt5.uic import loadUi

from api.instance import get_api
from api.plugins import SectionPlugin
from .plex import PlexController


class PlexSectionPlugin(SectionPlugin):
    def __init__(self):
        super().__init__()
        self.__widget = None
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__plex_controller = None

    def activate(self):
        path = os.path.join(self.__path, "section.ui")
        self.__widget = loadUi(path)
        # self.__widget.toolBox.removeItem(0)  # remove dummy page

        #plugins = api.pluginManager.getPluginsOfCategory("toolbox")
        #plugins.sort(key=lambda x: x.plugin_object.get_order())
        #for plugin in plugins:
        #    po = plugin.plugin_object
        #    po.activate()
        #    self.widget.toolBox.addItem(po.get_widget(), po.get_section_name())

        self.__plex_controller = PlexController(self._api.brain, self.__widget.graphicsView)

    def get_widget(self):
        return self.__widget

    def get_section_name(self):
        return 'Brain'
