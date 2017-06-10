import os

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

__history = InMemoryHistory()


def get_prompt(q):
    if os.environ.get("DEBUG"):  # todo move to API
        return input(q)
    else:
        return prompt(q, history=__history)  # Run with DEBUG env
