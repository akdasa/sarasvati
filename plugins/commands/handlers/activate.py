from plugins.commands.commands import ActivateCommand

__NOTHING_ERR = "No thought '{}' found to activate."
__AMBIGUOUS_ERR = "Multiple thoughts ({}) found. Unable to activate."


def activate(api, args):
    title = args.get("arg")
    search = api.brain.search.by_title(title)
    thought = api.get_one(search,
                          __NOTHING_ERR.format(title),
                          __AMBIGUOUS_ERR.format(len(search)))
    api.brain.commands.execute(ActivateCommand(thought))


