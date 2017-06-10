from plugins.commands.commands import DeleteCommand
from sarasvati.commands import CommandException

__NOTHING_ERR = "No thought '{}' found to delete."
__AMBIGUOUS_ERR = "Multiple thoughts ({}) found. Unable to delete."
__NO_ACTIVE_ERR = "No activated thought to delete."


def delete(api, args):
    title = args.get("arg")

    if title:
        search = api.brain.search.by_title(title)
        thought = api.get_one(search,
                              __NOTHING_ERR.format(title),
                              __AMBIGUOUS_ERR.format(len(search)))
        api.brain.commands.execute(DeleteCommand(thought))
        return "Thought '{}' deleted".format(title)
    else:
        if api.brain.state.active_thought is not None:
            api.brain.commands.execute(DeleteCommand(api.brain.state.active_thought))
            return "Thought '{}' deleted".format(api.brain.state.active_thought.title)
        else:
            raise CommandException(__NO_ACTIVE_ERR)
