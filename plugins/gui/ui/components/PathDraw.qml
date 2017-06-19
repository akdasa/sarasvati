import QtQuick 2.5

Item {
    id: rootDraw

    property int lineWidth: 3
    property color lineColor: "#000"
    property int point1x
    property int point1y
    property int point2x
    property int point2y
    property bool dottedAnimation: true

    Item {
        id: priv
        property int multiple: dottedAnimation ? 10 : 5;
    }

    Behavior on opacity {
        PropertyAnimation{ duration:1000 }
    }

    PathView {
        id: rooPath
        anchors.fill: parent
        model: Math.sqrt(Math.pow(Math.abs(point1x - point2x),2)+ Math.pow(Math.abs(point1y - point2y),2))/priv.multiple
        interactive: false
        delegate: Rectangle{ color:lineColor;width:lineWidth;height:lineWidth;radius: lineWidth/2;smooth: true }
        path: Path {
            startX: point1x; startY: point1y
            PathLine {
                x:point2x; y: point2y
            }
        }

        SequentialAnimation{
            running: dottedAnimation
            loops: -1
            PropertyAnimation{ target: rooPath; property: "offset"; to: 0; duration: 0 }
            PropertyAnimation{ target: rooPath; property: "offset"; to: 1; duration: 1500 }
        }
    }
}