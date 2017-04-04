from api.commands import Command


class ListCommand(Command):
    def execute(self, api):
        for thought in api.database.find(None) or []:
            print(thought.title)

    def revert(self, api):
        pass
