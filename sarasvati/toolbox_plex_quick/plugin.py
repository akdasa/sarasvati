import os

from PyQt5.uic import loadUi

from api.plugins import ToolboxPlugin
from .controller import Controller


class BrainQuickToolboxPlugin(ToolboxPlugin):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.widget = None
        self.path = os.path.dirname(os.path.abspath(__file__))

    def activate(self):
        path = os.path.join(self.path, "widget.ui")
        self.widget = loadUi(path)

        self.controller = Controller(self.widget)

    def get_widget(self):
        return self.widget

    def get_section_name(self):
        return 'Actions'

    def get_order(self):
        return -999  # 'Actions' tab should be first
