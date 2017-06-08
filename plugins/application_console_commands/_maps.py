from sarasvati.commands import CommandException


def show_command_map(api, args):
    args_count = len(args)

    if args_count == 1:
        title = args[0]
        result = api.brain.search.by_title(title, operator="~~")
        result_len = len(result)
        if result_len == 0:
            raise CommandException("No thought found")
        elif result_len > 1:
            raise CommandException("More than one thought found")
        else:
            return [result[0]]
    elif args_count == 0:
        if not api.brain.state.active_thought:
            raise CommandException("No active thought")
        return [api.brain.state.active_thought]
    else:
        raise CommandException("'show' takes 0-1 arguments but {} were given".format(args_count))
