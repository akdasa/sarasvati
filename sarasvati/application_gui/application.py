import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from api.models import Brain


class SarasvatiGuiApplication:
    def __init__(self, storage_plugin, section_plugins):
        """
        Initializes new instance of the SarasvatiConsoleApplication class.
        :type command_plugins: [CommandsPlugin]
        :type storage_plugin: DatabasePlugin
        :param storage_plugin: Database 
        :param command_plugins: Commands
        """
        storage = storage_plugin.get_storage()
        self.__brain = Brain(storage)
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__section_plugins = section_plugins

    def run(self):
        app = QApplication(sys.argv)
        widget = loadUi(os.path.join(self.__path, 'main.ui'))
        self.__init_sections(widget, self.__section_plugins)

        widget.show()
        sys.exit(app.exec_())

    @staticmethod
    def __init_sections(widget, plugins):
        for plugin in plugins:
            #po.activate()
            widget.tabWidget.addTab(plugin.get_widget(), plugin.get_section_name())
