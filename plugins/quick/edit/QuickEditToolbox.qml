import QtQuick 2.7
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QuickEditToolbox 1.0

import "controller.js" as Controller

QuickEditToolbox {
    id: self

    ColumnLayout {
        anchors.left: parent.left
        anchors.right: parent.right

        // Title
        TextField {
            id: title
            placeholderText: "Title"
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: false

            onTextChanged: Controller.update()
        }

        // Description
        TextArea {
            id: description
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: false

            onTextChanged: Controller.update()
        }

        // Create thought buttons
        RowLayout {
            id: buttonsRow
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: false

            Button {
                text: "Child"
                Layout.fillWidth: true
                onClicked: Controller.create("child")
            }
            Button {
                text: "Parent"
                onClicked: Controller.create("parent")
            }
            Button {
                text: "Reference"
                onClicked: Controller.create("reference")
            }
        }
    }

    Connections {
        onActivated: {
            title.enabled = enabled
            description.enabled = enabled
            buttonsRow.enabled = enabled

            title.text = thought_title
            description.text = thought_description
        }
    }
}
