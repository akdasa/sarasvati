import QtQuick 2.0
import QuickEditToolbox 1.0
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

QuickEditToolbox {
    id: self

    ColumnLayout {
        TextField {
            id: title
            placeholderText: "Title"
            anchors.left: parent.left
            anchors.right: parent.right

            onEditingFinished: function() {
                self.changed(title.text, description.text)
            }
        }

        TextArea {
            id: description
            anchors.left: parent.left
            anchors.right: parent.right

            onEditingFinished: function() {
                self.changed(title.text, description.text)
            }
        }
    }

    Connections {
        onActivated: {
            title.text = thought_title
            description.text = thought_description
        }
    }
}
