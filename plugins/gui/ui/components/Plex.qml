import QtQuick 2.5
import QtQuick.Controls 1.4

import "plex.js" as Plex

Rectangle {
    id: self

    /*Canvas {
        id: canvas
        anchors.fill: parent
        antialiasing: true
        contextType: "2d"
        renderStrategy: Canvas.Cooperative

        property real i : 0

        onPaint: {
            context.clearRect(0, 0, width, height)

            for (var hash in Plex.links) {
                var link = Plex.links[hash];
                var node = link["from"];
                var node2 = link["to"];

                context.strokeStyle = Qt.rgba(0, 0, 0, node.opacity / 3)

                context.beginPath();
                context.moveTo(node.x + node.width/2, node.y+node.height/2);
                context.lineTo(node2.x + node2.width/2, node2.y+node2.height/2);
                context.stroke();
            }
        }
    }*/

    Connections {
        target: plex

        onCommand: {
            Plex.processCommand(command)
        }
    }
}
