from sarasvati.commands import CommandException


def activate(api, args):
    args_count = len(args)
    if args_count != 1:
        raise CommandException("'activate' takes 1 argument but {} were given".format(args_count))

    title = args[0]
    result = api.brain.search.by_title(title)
    return [api.get_one(result)]


def set_title_or_description(api, args):
    args_count = len(args)
    if args_count == 2:
        title = args[0]
        new_title_or_desc = args[1]
        result = api.brain.search.by_title(title)
        return [api.get_one(result), new_title_or_desc]
    elif args_count == 1:
        title_or_desc = args[0]
        if not api.brain.state.active_thought:
            raise CommandException("No active thought")
        return [api.brain.state.active_thought, title_or_desc]
    else:
        raise CommandException("'title' takes 1 or 2 arguments but {} were given".format(args_count))


def delete(api, args):
    if len(args) == 1:
        title = args[0]
        result = api.brain.search.by_title(title)
        return [api.get_one(result)]
    elif len(args) == 0:
        if not api.brain.state.active_thought:
            raise CommandException("No active thought")
        return [api.brain.state.active_thought]
    else:
        raise Exception("'delete' takes 0 or 1 argument but {} were given".format(len(args)))


def link(api, args):
    if len(args) == 3:
        src_title = args[0]
        dst_title = args[1]
        kind = args[2]

        src_thought = api.get_one(api.brain.search.by_title(src_title))
        dst_thought = api.get_one(api.brain.search.by_title(dst_title))
        return [src_thought, dst_thought, kind]
    elif len(args) == 2:
        dst_title = args[0]
        kind = args[1]

        if not api.brain.state.active_thought:
            raise CommandException("No active thought")
        dst_thought = api.get_one(api.brain.search.by_title(dst_title))
        return [api.brain.state.active_thought, dst_thought, kind]
    else:
        raise CommandException("'link' takes 2-3 arguments but {} were given".format(len(args)))
