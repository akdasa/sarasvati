from plugins.commands.commands import LinkCommand
from sarasvati.commands import CommandException

__NOTHING_ERR = "No thought '{}' found to update."
__AMBIGUOUS_ERR = "Multiple thoughts ({}) found. Unable to update."
__NO_ACTIVE_ERR = "No activated thought to update."


def link(api, args):
    title = args.get("arg")
    as_ = args.get("as")
    to_ = args.get("to")

    if title:
        search = api.brain.search.by_title(title)
        thought = api.get_one(search,
                              __NOTHING_ERR.format(title),
                              __AMBIGUOUS_ERR.format(len(search)))
    else:
        if not api.brain.state.active_thought:
            raise CommandException(__NO_ACTIVE_ERR)
        thought = api.brain.state.active_thought

    if to_:
        search = api.brain.search.by_title(to_)
        to_thought = api.get_one(search,
                                 __NOTHING_ERR.format(to_),
                                 __AMBIGUOUS_ERR.format(len(to_)))
    else:
        raise CommandException("No 'to' argument specified")

    if not as_:
        raise CommandException("No 'as' argument specified")

    api.brain.commands.execute(LinkCommand(to_thought, thought, as_))
    return "'{}' linked to '{}' as {}".format(thought.title, to_thought.title, as_)
