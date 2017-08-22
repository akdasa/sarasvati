import QtQuick 2.7
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QuickEditToolbox 1.0

import "controller.js" as Controller

QuickEditToolbox {
    id: self

    ColumnLayout {
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
    }

    Connections {
        onActivated: {
            title.enabled = enabled
            description.enabled = enabled

            title.text = thought_title
            description.text = thought_description
        }
    }
}
