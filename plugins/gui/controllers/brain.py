from PyQt5.QtCore import QObject, pyqtSlot

from sarasvati import get_api


class BrainController(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(str, name="activate")
    def activate(self, key):
        thought = get_api().brain.search.by_key(key)
        get_api().brain.state.activate(thought)
