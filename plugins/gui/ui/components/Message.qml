import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

Rectangle {
    property alias message : textMetrics.text

    TextMetrics {
        id: textMetrics
        text: "Hello World"
    }

    Rectangle {
        width: textMetrics.width
        height: textMetrics.height
        color: "#fff"
        radius: 5

        Text {
            text: textMetrics.text
            font: textMetrics.font
            anchors.centerIn: parent
        }
    }

    SequentialAnimation on opacity {
        id: opacityAnimation
        NumberAnimation {
            from: 0
            to: 1
            duration: 100
        }
        PauseAnimation { duration: 3000 }
        NumberAnimation {
            from: 1
            to: 0
            duration: 500
            onRunningChanged: {
                if (!running) {
                    rect.destroy();
                }
            }
        }
    }
}
