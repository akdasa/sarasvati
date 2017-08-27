from sarasvati.commands import CommandResult, ActivateCommand
from sarasvati.exceptions import CommandException


def activate(api, args):
    title = args.arg or args.title
    key = args.key

    if not (title or key):  # no title and key specified
        raise CommandException("No title or key specified")
    if title and key:  # title and key specified both
        raise CommandException("The name and key can not be used at the same time")

    thought = None
    if title:
        thought = api.utilities.find_one_by_title(title)
    elif key:
        thought = api.storage.get(key)
        if not thought:
            raise CommandException("No thought found with '{}' key".format(key))

    api.brain.commands.execute(ActivateCommand(thought))

    return CommandResult(thought, message="Thought '{}' activated".format(thought.title))
