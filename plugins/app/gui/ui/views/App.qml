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
            id: p
            Layout.fillWidth: true
        }

        Panel {
            objectName: "panel"
            Layout.maximumWidth: 400
            Layout.minimumWidth: 250
        }
    }

    Connections {
        target: processor
        onCommandResult: {
            var component = Qt.createComponent("../components/Message.qml")
            var link = component.createObject(root, {"message": message, "x": 10, "y": 10})
            //console.log("Error loading component:", component.errorString());
        }
    }

    onWidthChanged: {
        plex.on_resize(p.width, p.height)
    }
    onHeightChanged: {
        plex.on_resize(p.width, p.height)
    }
}
