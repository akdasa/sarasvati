from plugins.commands.commands import ActivateCommand
from sarasvati.commands import CommandException


def activate(api, args):
    title = args.get("arg") or args.get("title")

    if not title:
        raise CommandException("No title specified")

    thought = api.find_one_by_title(title)
    api.brain.commands.execute(ActivateCommand(thought))
