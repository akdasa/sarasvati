import os

from PyQt5.uic import loadUi

from api.plugins import ToolboxPlugin
from .controller import Controller


class BrainQuickToolboxPlugin(ToolboxPlugin):
    def __init__(self):
        super().__init__()
        self.__controller = None
        self.__widget = None
        self.__path = os.path.dirname(os.path.abspath(__file__))

    def activate(self):
        path = os.path.join(self.__path, "widget.ui")
        self.__widget = loadUi(path)
        self.__controller = Controller(self.__widget)

    def get_widget(self):
        return self.__widget

    def get_section_name(self):
        return 'Actions'

    def get_order(self):
        return -999  # 'Actions' tab should be first
