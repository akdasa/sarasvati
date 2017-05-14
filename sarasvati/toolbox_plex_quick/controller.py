from api.instance import get_api


class Controller:
    def __init__(self, widget):
        self.__is_modified = False
        self.__widget = widget
        self.__thought = None
        self.__api = get_api()

        # subscribe for widget's events
        self.__widget.createChildButton.clicked.connect(self.__on_create_child_button_clicked)
        self.__widget.createParentButton.clicked.connect(self.__on_create_parent_button_clicked)
        self.__widget.createReferenceButton.clicked.connect(self.__on_create_reference_button_clicked)
        self.__widget.title.textChanged.connect(self.__on_title_text_changed)
        self.__widget.description.textChanged.connect(self.__on_description_text_changed)

        # app's events
        self.__api.events.thoughtSelected.subscribe(self.__on_thought_selected)

    def __update_controls(self, thought):
        self.__widget.title.setText(thought.title)
        self.__widget.description.setText(thought.description)

        self.__widget.createChildButton.setEnabled(thought is not None)
        self.__widget.createParentButton.setEnabled(thought is not None)
        self.__widget.createReferenceButton.setEnabled(thought is not None)

    def __on_thought_selected(self, thought):
        if self.__thought and self.__is_modified:
            self.__api.actions.update_thought(self.__thought)
            self.__is_modified = False
        self.__thought = thought
        self.__update_controls(thought)

    def __on_create_child_button_clicked(self):
        self.__api.actions.create_linked_thought(self.__thought, "child", "Child Node")

    def __on_create_parent_button_clicked(self):
        self.__api.actions.create_linked_thought(self.__thought, "parent", "Parent Node")

    def __on_create_reference_button_clicked(self):
        self.__api.actions.create_linked_thought(self.__thought, "reference", "Reference Node")

    def __on_title_text_changed(self):
        title = self.__widget.title.toPlainText()
        if self.__thought and self.__thought.title != title:
            self.__thought.title = title
            self.__api.actions.updating_thought(self.__thought)
            self.__is_modified = True

    def __on_description_text_changed(self):
        description = self.__widget.description.toPlainText()
        if self.__thought and self.__thought.description != description:
            self.__thought.description = description
            self.__api.actions.updating_thought(self.__thought)
            self.__is_modified = True
