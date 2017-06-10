import os

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

__history = InMemoryHistory()
__simple_prompt = os.environ.get("SIMPLE_PROMPT")


def get_prompt(q):
    if __simple_prompt:
        return input(q)
    else:
        return prompt(q, history=__history)
