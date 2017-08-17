import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3

Rectangle {
    color: "whitesmoke"

    ColumnLayout {
        anchors.fill: parent

        CommandPrompt {
            color: "whitesmoke"
            anchors.margins: 5
            Layout.fillWidth: true
            Layout.margins: 5
            height: 50;
        }

        Rectangle {
            color: "whitesmoke";
            Layout.fillWidth: true;
            Layout.fillHeight: true
        }
    }
}
