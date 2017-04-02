
class Processor:
    def __init__(self, api=None, default_command=None):
        self.__handlers = {}
        self.__api = api
        self.__default_command = default_command

    def register(self, command):
        if not command.NAME:
            raise Exception("Command must have NAME property")
        self.__handlers[command.NAME] = command

    def execute(self, prompt):
        if prompt in self.__handlers.keys():
            command = self.__handlers[prompt]()
            command.execute(self.__api)
        elif self.__default_command is not None:
            command = self.__default_command()
            command.execute(self.__api)
        else:
            print("Unknown command")

    def prompt(self):
        return "> "
