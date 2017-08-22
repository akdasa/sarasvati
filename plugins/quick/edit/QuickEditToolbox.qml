import QtQuick 2.7
import QuickEditToolbox 1.0
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

import "controller.js" as Controller

QuickEditToolbox {
    id: self

    ColumnLayout {
        TextField {
            id: title
            placeholderText: "Title"
            anchors.left: parent.left
            anchors.right: parent.right

            onEditingFinished: Controller.update()
            onTextChanged: Controller.update(false)
        }

        TextArea {
            id: description
            anchors.left: parent.left
            anchors.right: parent.right

            onEditingFinished: Controller.update()
            onTextChanged: Controller.update(false)
        }
    }

    Connections {
        onActivated: {
            title.text = thought_title
            description.text = thought_description
        }
    }
}
