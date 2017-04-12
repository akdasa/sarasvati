from api.plugins import CommandException


def show_command_map(api, args):
    args_count = len(args)

    if args_count == 1:
        title = args[0]
        query = {"field": "definition.title", "operator": "~~", "value": title}
        result = api.storage.search(query)
        result_len = len(result)
        if result_len == 0:
            raise CommandException("No thought found")
        elif result_len > 1:
            raise CommandException("More than one thought found")
        else:
            return [result[0]]
    elif args_count == 0:
        if not api.active_thought:
            raise CommandException("No active thought")
        return [api.active_thought]
    else:
        raise CommandException("'show' takes 0-1 arguments but {} were given".format(args_count))
