import QtQuick 2.5
import QtQuick.Controls 1.4

import "plex.js" as Plex

Rectangle {
    id: self
    anchors.fill: parent

     Connections {
        target: plex

        onCommandResult: {
            Plex.processCommand(command)
        }
    }
}
