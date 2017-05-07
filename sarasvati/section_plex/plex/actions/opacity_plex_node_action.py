from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

from .plex_node_action import PlexNodeAction


class OpacityPlexNodeAction(PlexNodeAction):
    def __init__(self, plex_node, start_opacity, end_opacity):
        super().__init__(plex_node)
        self.animation = QPropertyAnimation(plex_node, b'opacity')
        self.animation.setDuration(500)
        self.animation.setStartValue(start_opacity)
        self.animation.setEndValue(end_opacity)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()
        self.animation.finished.connect(self.__on_animation_finished)

    def __on_animation_finished(self):
        self.completed.notify(self)
