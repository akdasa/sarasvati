from api.instance import get_api


class Controller:
    def __init__(self, widget):
        self.widget = widget
        self.active_thought = None
        self.__api = get_api()

        # subscribe for widget's events
        self.widget.createChildButton.clicked.connect(self.__on_create_child_button_clicked)
        self.widget.createParentButton.clicked.connect(self.__on_create_parent_button_clicked)
        self.widget.createJumpButton.clicked.connect(self.__on_create_jump_button_clicked)
        self.widget.title.textChanged.connect(self.__on_title_text_changed)
        self.widget.description.textChanged.connect(self.__on_description_text_changed)

        # app's events
        self.__api.events.thoughtSelected.subscribe(self.__on_thought_selected)

    def __update_controls(self, thought):
        self.widget.title.setText(thought.title)
        self.widget.description.setText(thought.description)

    def __on_thought_selected(self, thought):
        self.active_thought = thought
        self.__update_controls(thought)

    def __on_create_child_button_clicked(self):
        if self.active_thought is None:
            self.active_thought = self.__api.actions.create_thought("New Node")
        else:
            self.__api.actions.create_linked_thought(self.active_thought, "parent->child", "Child Node")
            pass

    def __on_create_parent_button_clicked(self):
        if self.active_thought is not None:
            pass
            #self.__api.actions.create_linked_thought(self.active_thought, "child->parent", "Parent Node")

    def __on_create_jump_button_clicked(self):
        if self.active_thought is not None:
            pass
            #self.__api.actions.create_linked_thought(self.active_thought, "jump", "Jump Node")

    def __on_title_text_changed(self):
        if self.active_thought:
            self.active_thought.title = self.widget.title.toPlainText()
            self.__api.actions.update_thought(self.active_thought)

    def __on_description_text_changed(self):
        if self.active_thought:
            self.active_thought.description =  self.widget.description.toPlainText()
            self.__api.actions.update_thought(self.active_thought)
