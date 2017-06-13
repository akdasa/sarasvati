from plugins.commands.commands import DeleteCommand
from plugins.processor.processor import CommandResult
from sarasvati.commands import CommandException


def delete(api, args):
    title = args.arg or args.title
    active = api.brain.state.active_thought

    if not title and not active:
        raise CommandException("No title specified nor activated thought")

    thought = api.utilities.find_one_by_title(title) if title else active

    api.execute(DeleteCommand(thought))

    return CommandResult(thought, message="Thought '{}' deleted".format(thought.title))
