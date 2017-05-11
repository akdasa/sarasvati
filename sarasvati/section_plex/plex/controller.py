from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView

from api.instance import get_api
from .plex import Plex
from .layout import PlexLayout
from .layout_action_executor import PlexLayoutActionExecutor
from .scene import PlexScene
from .state_diff import PlexStateDiff


class PlexController:
    def __init__(self, brain, view):
        self.scene = None
        self.brain = brain
        self.view = view
        self.plex = Plex(self.brain)
        self.differ = PlexStateDiff()
        self.layout = PlexLayout()
        self.active_thought = None
        self.__api = get_api()

        self.__api.events.thoughtSelected.subscribe(self.__on_thought_selected)
        self.__api.events.thoughtCreated.subscribe(self.__on_thought_created)
        self.__api.events.thoughtChanged.subscribe(self.__on_thought_changed)

        self.__set_up_view_widget()
        self.actions_executor = PlexLayoutActionExecutor(self.scene)

        root_thought = self.brain.search.by_title("Brain")[0]  # todo get_root_thought()
        self.activate(root_thought)

        self.__api.events.thoughtSelected.notify(root_thought)

    def activate(self, thought):
        self.brain.search.by_id(thought.key)  # TODO load lazy thought

        self.active_thought = thought
        new_state = self.plex.activate(thought)
        actions = self.layout.change_to(new_state)
        self.actions_executor.run(actions)

    def __set_up_view_widget(self):
        self.scene = PlexScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setSceneRect(0, 0, 25, 25)
        self.view.show()

    def __on_thought_selected(self, thought):
        self.activate(thought)

    def __on_thought_created(self, thought):
        if self.active_thought:
            self.activate(self.active_thought)
        else:
            self.activate(thought)

    def __on_thought_changed(self, thought):
        node = self.scene.get_node(thought)
        if node:
            node.update()
        if self.active_thought == thought:
            self.activate(self.active_thought)
