import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3

Rectangle {
    color: "whitesmoke"
    default property alias data: column.data

    function append(toolbox) {
        toolbox.parent = column
        toolbox.Layout.fillWidth = true
        toolbox.Layout.margins = 5
    }

    ColumnLayout {
        id: column
        width: parent.width
    }
}
