from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

from .plex_node_action import PlexNodeAction


class MovePlexNodeAction(PlexNodeAction):
    def __init__(self, plex_node, point):
        super().__init__(plex_node)
        self.animation = QPropertyAnimation(plex_node, b'pos')
        self.animation.setDuration(500)
        self.animation.setStartValue(plex_node.pos())
        self.animation.setEndValue(point)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()
        self.animation.finished.connect(self.__on_animation_finished)

    def __on_animation_finished(self):
        self.completed.notify(self)
