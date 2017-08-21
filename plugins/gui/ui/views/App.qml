import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import "../components"

ApplicationWindow {
    id: root
    visible: true
    width: 640
    height: 480

    SplitView {
        anchors.fill: parent
        orientation: Qt.Horizontal

        Plex {
            Layout.fillWidth: true
        }

        Panel {
            objectName: "panel"
            Layout.maximumWidth: 400
            Layout.minimumWidth: 250
        }
    }
}
