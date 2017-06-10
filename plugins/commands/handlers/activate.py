from plugins.commands.commands import ActivateCommand


def activate(api, args):
    thought = api.find_one_by_title(args.get("arg"))
    api.brain.commands.execute(ActivateCommand(thought))
