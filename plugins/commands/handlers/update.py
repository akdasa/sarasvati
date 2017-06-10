from plugins.commands.commands import SetTitleCommand, SetDescriptionCommand
from sarasvati.commands import CommandException

__NOTHING_ERR = "No thought '{}' found to update."
__AMBIGUOUS_ERR = "Multiple thoughts ({}) found. Unable to update."
__NO_ACTIVE_ERR = "No activated thought to update."


def update(api, args):
    arg = args.get("arg")
    title = args.get("title")
    desc = args.get("desc")
    result = []

    if not title and not desc:
        raise CommandException("Nothing to do")

    if arg:
        search = api.brain.search.by_title(arg)
        thought = api.get_one(search,
                              __NOTHING_ERR.format(title),
                              __AMBIGUOUS_ERR.format(len(search)))
    else:
        if not api.brain.state.active_thought:
            raise CommandException(__NO_ACTIVE_ERR)
        thought = api.brain.state.active_thought

    if title:
        result.append("Title of '{}' updated to '{}'".format(thought.title, title))
        api.brain.commands.execute(SetTitleCommand(thought, title))

    if desc:
        result.append("Description of '{}' updated to '{}'".format(thought.title, desc))
        api.brain.commands.execute(SetDescriptionCommand(thought, desc))

    return result
