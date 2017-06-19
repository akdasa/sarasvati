import QtQuick 2.0

Rectangle {
    id: self

    color: "whitesmoke"
    width: childrenRect.width + 25
    height: childrenRect.height + 10
    border.color: "grey"
    border.width: 1
    radius: 10

    property alias title : title.text
    property string key

    signal destroyed123()

    Text {
        id: title
        anchors.centerIn: parent
        font.pointSize: 18
    }

    MouseArea {
        anchors.fill: parent
        onClicked: { brain.activate(key) }
    }

    function show() {
        self.scale = 0
        scaleAnimation.restart()
        z = 1
    }

    function move(x, y) {
        movePath.startX = self.x + self.width/2
        movePath.startY = self.y + self.height/2
        moveEnd.x = x
        moveEnd.y = y
        moveAnimation.restart()
    }

    function selfDestroy() {
        opacityAnimation.start()
        scaleAnimation.to = 0
        scaleAnimation.easing.overshoot = 0
        scaleAnimation.restart()
    }


    PathAnimation {
        id: moveAnimation
        target: self
        easing.type: Easing.InOutCubic
        duration: 1000
        anchorPoint: Qt.point(self.width/2, self.height/2)

        path: Path {
            id: movePath
            PathLine { id: moveEnd }
        }
    }

    NumberAnimation on opacity {
        id: opacityAnimation
        to: 0
        duration: 1500
        running: false

        onRunningChanged: {
            if (!running) {
                self.destroyed123();
                self.destroy();
            }
        }
    }

    NumberAnimation on scale {
        id: scaleAnimation
        to: 1
        duration: 1000
        running: false
        easing.type: Easing.InOutQuad
    }

}