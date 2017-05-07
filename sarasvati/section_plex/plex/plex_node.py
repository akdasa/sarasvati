from PyQt5.QtCore import QRectF, Qt, QMarginsF, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsWidget
from api.instance import get_api


class PlexNode(QGraphicsWidget):
    maxBounding = QRectF(0, 0, 150, 150)
    margins = QMarginsF(10, 10, 10, 10)

    def __init__(self, thought):
        super(PlexNode, self).__init__()
        self.thought = thought
        self.boundingRect = QRectF(0, 0, 0, 0)
        self.animations = []
        self.nexPos = QPointF(0, 0)

    # noinspection PyMethodOverriding
    def paint(self, painter, option, widget):
        background_rect = self.boundingRect.marginsAdded(self.margins)

        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setBrush(QBrush(QColor(127, 255, 127)))
        painter.drawRoundedRect(background_rect, 10, 10)

        tbr = painter.drawText(self.maxBounding, Qt.TextWordWrap, self.thought.title)

        painter.setPen(QPen(QColor(0, 0, 0, 127)))
        dbr = painter.drawText(self.maxBounding.translated(0, tbr.height()),
                               Qt.TextWordWrap, self.thought.definition.description)

        self.boundingRect = tbr.united(dbr)
        self.resize(self.boundingRect.width(), self.boundingRect.height())

    def boundingRect(self):
        return self.boundingRect

    def mousePressEvent(self, event):
        get_api().events.thoughtSelected.notify(self.thought)
