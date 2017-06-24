// ======================= //
// Plex commands processor //
// ======================= //
function processCommand(c) {
    var cmd = c["cmd"]
    var key = c["key"]

    switch (cmd) {
        case "add":        add(key, c["title"], c["x"], c["y"]); break;
        case "move":       move_to(key, c["x"], c["y"]); break;
        //case "set_pos_to": set_pos_to(key, c["x"], c["y"]); break;
        case "remove":     remove(key); break;
        case "link":       add_link(c["from"], c["to"]); break;
    }
}

// node commands

function add(key, title, x ,y) {
    var node = nodeComponent.createObject(self, {
        "key": key,
        "title": title
    })

    node.x = x + self.width / 2 - node.width/2
    node.y = y + self.height / 2 - node.height/2

    //node.moved.connect(canvas_repaint)
    node.show()
    nodes[key] = node
}

function move_to(key, x, y) {
    nodes[key].move(x + self.width / 2, y + self.height / 2)
}

function set_pos_to(key, x, y) {
    var entity = nodes[key]
    entity.x = x + self.width / 2  - entity.width / 2
    entity.y = y + self.height / 2 - entity.height / 2
}

function remove(key) {
    var entity = nodes[key]
    entity.destroyed123.connect(function() {
        delete_link(entity.key)
    })
    entity.selfDestroy()
}

// link commands

function add_link(key, key2) {
    if (links[key+key2]) {
        print("Already exist")
        return;
    }
    if (links[key2+key]) {
        print("Already exist")
        return;
    }

    var entity = nodes[key]
    var entity2 = nodes[key2]

    var link = linkComponent.createObject(self, {
        "point1x": Qt.binding(function() { return entity.x + entity.width/2 }),
        "point1y": Qt.binding(function() { return entity.y + entity.height/2 }),
        "point2x": Qt.binding(function() { return entity2.x + entity2.width/2 }),
        "point2y": Qt.binding(function() { return entity2.y + entity2.height/2 })
    })
    //var link = { "from": entity, "to": entity2 }

    //links[key+key2] = link
    links[key2+key] = link
}

function delete_link(key) {
    for (var idx in links) {
        var linkHash = idx
        print("D: " + linkHash)
        if (linkHash.startsWith(key) || linkHash.endsWith(key)) {
            var lll = links[linkHash];
            print("DELETING:" + linkHash)
            lll.destroy()
            delete links[linkHash]
        }
    }
    print("LNKS LEN" + Object.keys(links).length)
}

// Canvas

function canvas_repaint() {
    canvas.requestPaint();
}

// state

var nodes = {}
var links = {}
var nodeComponent = Qt.createComponent("PlexNode.qml")
var linkComponent = Qt.createComponent("Link.qml")
