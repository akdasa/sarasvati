from sarasvati.commands import CommandResult, LinkCommand
from sarasvati.exceptions import CommandException


def link(api, args):
    title = args.get("arg")
    to_ = args.get("to")
    as_ = args.get("as")
    active = api.brain.state.active_thought

    # validate
    if not title and not active:
        raise CommandException("No title specified nor activated thought")
    if not to_:
        raise CommandException("No 'to' argument specified")
    if not as_:
        raise CommandException("No 'as' argument specified")
    if as_ not in ["child", "parent", "reference"]:
        raise CommandException("Wrong link type in 'as' argument")

    # get required data
    thought = api.utilities.find_one_by_title(title) if title else active
    to_thought = api.utilities.find_one_by_title(to_, arg_name="to")

    # execute
    result = api.brain.commands.execute(LinkCommand(to_thought, thought, as_))
    return CommandResult(result, message="'{}' linked to '{}' as {}".format(thought.title, to_thought.title, as_))
