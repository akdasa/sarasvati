from PyQt5.QtCore import QPointF, QMarginsF
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene

from .node import PlexNode


class PlexScene(QGraphicsScene):
    def get_node(self, thought) -> PlexNode:
        for item in self.items():
            if item.thought.key == thought.key:
                return item

    def get_node_by_id(self, thought_id) -> PlexNode:
        for item in self.items():
            if item.thought.key == thought_id:
                return item

    def drawBackground(self, painter, rect):
        return
        drawn_from = []
        painter.setRenderHint(QPainter.Antialiasing)
        for item in self.items():
            all_links = item.thought.links.all
            for key in all_links:
                link = all_links[key]
                link_id = link.key
                link_kind = link.kind
                node = self.get_node_by_id(link_id)
                if node is not None and node not in drawn_from:
                    if link_kind == "parent":
                        self.__draw_link(painter, node, item)
                    if link_kind == "reference":
                        self.__draw_jump_link(painter, item, node)
            drawn_from.append(item)

    @staticmethod
    def __draw_link(painter, src, dst):
        margins = QMarginsF(10, 10, 10, 10)
        opacity = min(dst.opacity(), src.opacity()) * 255

        src_geometry = src.geometry().marginsAdded(margins)
        dst_geometry = dst.geometry().marginsAdded(margins)
        src_center = src_geometry.center()
        dst_center = dst_geometry.center()
        src_offset = QPointF(0, src_geometry.height() / 2)
        dst_offset = QPointF(0, dst_geometry.height() / 2)

        start_point = src_center + src_offset
        end_point = dst_center - dst_offset
        control_point1 = start_point + QPointF(0, 50)
        control_point2 = end_point - QPointF(0, 50)

        cubic_path = QPainterPath(start_point)
        cubic_path.cubicTo(control_point1, control_point2, end_point)

        painter.setPen(QPen(QColor(0, 0, 0, opacity)))
        painter.drawPath(cubic_path)


    @staticmethod
    def __draw_jump_link(painter, src, dst):
        margins = QMarginsF(10, 10, 10, 10)
        opacity = min(dst.opacity(), src.opacity()) * 255

        src_geometry = src.geometry().marginsAdded(margins)
        dst_geometry = dst.geometry().marginsAdded(margins)
        src_center = src_geometry.center()
        dst_center = dst_geometry.center()
        src_offset = QPointF(src_geometry.width() / 2, 0)
        dst_offset = QPointF(dst_geometry.width() / 2, 0)

        start_point = src_center + src_offset
        end_point = dst_center - dst_offset
        control_point1 = start_point + QPointF(50, 0)
        control_point2 = end_point - QPointF(50, 0)

        cubic_path = QPainterPath(start_point)
        cubic_path.cubicTo(control_point1, control_point2, end_point)

        painter.setPen(QPen(QColor(0, 0, 0, opacity)))
        painter.drawPath(cubic_path)