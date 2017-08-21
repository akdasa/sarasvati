import QtQuick 2.0
import QuickEditToolbox 1.0
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

QuickEditToolbox {
    ColumnLayout {
        TextField {
            id: title
            placeholderText: "Title"
            anchors.left: parent.left
            anchors.right: parent.right
        }

        TextArea {
            anchors.left: parent.left
            anchors.right: parent.right
        }
    }
}
