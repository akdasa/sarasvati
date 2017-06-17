function processCommand(command) {
    var cmd = command["cmd"]
    var key = command["key"]

    if (cmd == "add") {
        add(key, command["title"])
    } else if (cmd == "move_to") {
        move(key, command["x"], command["y"])
    } else if (cmd == "remove") {
        remove(key)
    }
}

function add(key, title) {
    var plexNode = component.createObject(self, {
        "x": self.width/2,
        "y": self.height/2,
        "title": title,
        "key": key
    })
    nodes[key] = plexNode
    return plexNode
}

function move(key, x, y) {
    var entity = nodes[key]
    entity.move(
        x + self.width / 2,
        y + self.height / 2)
}

function remove(key) {
    var entity = nodes[key]
    entity.selfDestroy()
}


var nodes = {}
var component = Qt.createComponent("PlexNode.qml")
