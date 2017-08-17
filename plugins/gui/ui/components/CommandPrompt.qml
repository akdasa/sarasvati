import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Rectangle {
    id: root

    TextField {
        id: self
        placeholderText: "Command Prompt"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        style: TextFieldStyle {
            background: Rectangle {
                color: "#eee"
                radius: 5
                border.color: "grey"
                border.width: 1
            }
        }

        onAccepted: {
            processor.execute(self.text)
            self.text = ""
        }

        Connections {
            target: processor

            onCommandResult: {
                response.text = message
                response.color = successful ? "green" : "red"
                opacityAnimation.restart()
            }
        }
    }

    Text {
        id: response
        text: ""
        color: "green"
        anchors.top: self.bottom
        anchors.margins: 5

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
            }
        }
    }
}
