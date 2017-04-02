from api.plugins import DatabasePlugin


class LocalDatabasePlugin(DatabasePlugin):
    def create(self):
        print("created")

    def delete(self):
        print("deleted")
