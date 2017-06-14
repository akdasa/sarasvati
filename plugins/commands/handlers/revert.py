def revert(api, args):
    arg = args.arg

    if arg in ["h", "history"]:
        for command in api.brain.commands.history:
            print(command.view or "??")

    else:
        api.brain.commands.revert()
