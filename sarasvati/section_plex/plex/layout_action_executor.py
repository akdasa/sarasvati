from PyQt5.QtCore import QPointF

from api.brain import Thought
from .actions import MovePlexNodeAction, OpacityPlexNodeAction
from .node import PlexNode


class PlexLayoutActionExecutor:
    def __init__(self, scene):
        self.scene = scene
        self.actions = []
        self.handlers = {}

        self.register_action("add", self.add_action)
        self.register_action("move_to", self.move_to_action)
        self.register_action("remove", self.remove_action)
        self.register_action("set_pos_to", self.set_pos_to_action)

    def register_action(self, name, action):
        self.handlers[name] = action

    def run(self, actions):
        for action in actions:
            handler = self.handlers[action.name]
            handler(action)

    def add_action(self, action):
        node = PlexNode(action.thought)
        action = OpacityPlexNodeAction(node, 0, 1)
        action.completed.subscribe(self.__on_action_completed)
        self.actions.append(action)
        self.scene.addItem(node)

    def remove_action(self, action):
        node = self.scene.get_node(action.thought)
        action = OpacityPlexNodeAction(node, node.opacity(), 0)
        action.completed.subscribe(self.__remove_node)
        action.completed.subscribe(self.__on_action_completed)
        self.actions.append(action)

    def move_to_action(self, action):
        node = self.scene.get_node(action.thought)

        point = None
        if type(action.data) is list:
            point = QPointF(action.data[0], action.data[1])
        elif type(action.data) is Thought:
            parent = self.scene.get_node(action.data)
            point = parent.pos()

        action = MovePlexNodeAction(node, point)
        action.completed.subscribe(self.__on_action_completed)
        self.actions.append(action)

    def set_pos_to_action(self, action):
        node1 = self.scene.get_node(action.thought)
        node2 = self.scene.get_node(action.data)
        node1.setPos(node2.pos())

    def __on_action_completed(self, action):
        action.completed.unsubscribe(self.__on_action_completed)
        self.actions.remove(action)

    def __remove_node(self, action):
        self.scene.removeItem(action.node)

