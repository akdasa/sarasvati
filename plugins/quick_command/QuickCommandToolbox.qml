import QtQuick 2.5
import QtQuick.Controls 1.4
import QuickCommandToolbox 1.0

QuickCommandToolbox {
    id: self
    height: prompt.height

    TextField {
        id: prompt
        placeholderText: "Prompt"
        anchors.left: parent.left
        anchors.right: parent.right

        onAccepted: {
            self.execute(prompt.text)
            prompt.text = ""
        }
    }
}
