from api.commands import Command


class ListCommand(Command):
    def __init__(self, api):
        super().__init__(api)

    def execute(self):
        for thought in self._api.database.find(None) or []:
            print(thought.title)

    def revert(self):
        pass
