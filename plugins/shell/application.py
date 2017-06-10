from sarasvati.application import SarasvatiApplication
from .prompt import get_prompt


class SarasvatiConsoleApplication(SarasvatiApplication):
    __QUIT_COMMANDS = ["/quit", "/q"]

    def __init__(self):
        super().__init__()

    def run(self):
        query = None
        while query not in self.__QUIT_COMMANDS:
            query = get_prompt(self.__prompt_state())
            self._processor.execute(query)

    def __prompt_state(self):
        thought = self._brain.state.active_thought
        if thought:
            return thought.title + "> "
        return "> "
