from plugins.commands.commands import DeleteCommand
from sarasvati.commands import CommandException


def delete(api, args):
    title = args.get("arg")
    active = api.brain.state.active_thought

    if not title and not active:
        raise CommandException("No title specified nor activated thought")

    if title:
        thought = api.utilities.find_one_by_title(title)
        api.execute(DeleteCommand(thought))
        return "Thought '{}' deleted".format(title)
    else:
        api.execute(DeleteCommand(active))
        return "Thought '{}' deleted".format(active.title)
