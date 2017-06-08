from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

__history = InMemoryHistory()


def get_prompt(q):
    return prompt(q, history=__history)
