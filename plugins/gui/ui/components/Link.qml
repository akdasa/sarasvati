import QtQuick 2.5

Item {
    id: link

    property alias point1x: line.point1x
    property alias point1y: line.point1y
    property alias point2x: line.point2x
    property alias point2y: line.point2y

    PathDraw {
        id:line
    }
}