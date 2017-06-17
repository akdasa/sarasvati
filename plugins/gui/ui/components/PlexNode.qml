import QtQuick 2.0

Rectangle {
    id: self

    color: "whitesmoke"
    width: childrenRect.width + 25
    height: childrenRect.height + 10
    border.color: "grey"
    border.width: 1
    radius: 5

    property alias title : title.text
    property string key

    Text {
        id: title
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: { plex.activate(key) }
    }

    function move(x, y) {
        movePath.startX = self.x
        movePath.startY = self.y
        moveEnd.x = x
        moveEnd.y = y
        moveAnimation.restart()
    }

    function selfDestroy() {
        opacityAnimation.start()
    }


    PathAnimation {
        id: moveAnimation
        target: self
        easing.type: Easing.InOutCubic
        duration: 1000
        /*anchorPoint: Qt.point(self.width/2, self.height/2)*/

        path: Path {
            id: movePath
            PathLine { id: moveEnd }
        }
    }

    NumberAnimation on opacity {
        id: opacityAnimation
        to: 0
        duration: 1000
        running: false

        onRunningChanged: {
            if (!running) {
                self.destroy();
            }
        }
    }

}