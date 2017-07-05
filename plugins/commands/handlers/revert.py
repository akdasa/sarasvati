from sarasvati.commands import CommandResult


def revert(api, args):
    arg = args.arg

    if arg in ["h", "history"]:
        for command in api.brain.commands.history:
            print(command.view or "??")
        return CommandResult(api.brain.commands.history, message=None)
    else:
        api.brain.commands.revert()
