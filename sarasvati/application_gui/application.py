import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from api.instance import get_api
from api.brain import Brain


class SarasvatiGuiApplication:
    def __init__(self, storage_plugin, section_plugins):
        """
        Initializes new instance of the SarasvatiGuiApplication class.
        :type storage_plugin: StoragePlugin
        :param storage_plugin: Storage 
        """
        storage = storage_plugin.get_storage()
        self.__brain = Brain(storage)
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__section_plugins = section_plugins
        get_api().brain = self.__brain

    def run(self):
        app = QApplication(sys.argv)
        widget = loadUi(os.path.join(self.__path, "main.ui"))
        self.__init_sections(widget, self.__section_plugins)

        widget.show()
        sys.exit(app.exec_())

    @staticmethod
    def __init_sections(widget, plugins):
        for plugin in plugins:
            plugin.activate()
            widget.tabWidget.addTab(plugin.get_widget(), plugin.get_section_name())
