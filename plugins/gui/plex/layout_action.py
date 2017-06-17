
class PlexLayoutAction:
    def __init__(self, thought, name, data=None):
        self.name = name
        self.thought = thought
        self.data = data

    def __eq__(self, other):
        return self.name == other.name and \
               self.thought == other.thought and \
               self.data == other.data

    def __repr__(self):
        return self.name + " " + str(self.thought) + " " + str(self.data)
