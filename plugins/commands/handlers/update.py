from plugins.commands.commands import SetTitleCommand, SetDescriptionCommand
from plugins.processor.processor import CommandResult
from sarasvati.commands import CommandException


def update(api, args):
    arg = args.get("arg")
    title = args.get("title")
    desc = args.get("desc")
    active = api.brain.state.active_thought

    # validation
    if not title and not desc:
        raise CommandException("Nothing to do")
    if not arg and not active:
        raise CommandException("No title specified nor activated thought")

    # get required data
    thought = api.utilities.find_one_by_title(arg) if arg else active

    # execute
    if title:
        api.brain.commands.execute(SetTitleCommand(thought, title))
    if desc:
        api.brain.commands.execute(SetDescriptionCommand(thought, desc))

    return CommandResult(thought, message="Thought '{}' updated".format(thought.title))
