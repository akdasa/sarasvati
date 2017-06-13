from plugins.commands.commands import SetTitleCommand, SetDescriptionCommand
from plugins.processor.processor import CommandResult
from sarasvati.commands import CommandException


def update(api, args):
    arg = args.get("arg")
    active = api.brain.state.active_thought

    # validation
    if not (args.title or args.desc):
        raise CommandException("Nothing to do")
    if not (arg or active):
        raise CommandException("No title specified nor activated thought")

    # get required data
    thought = api.utilities.find_one_by_title(arg) if arg else active

    # execute
    if args.title:
        api.execute(SetTitleCommand(thought, args.title))
    if args.desc:
        api.execute(SetDescriptionCommand(thought, args.desc))

    # result
    return CommandResult(thought, message="Thought '{}' updated".format(thought.title))
