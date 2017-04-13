from api.plugins import CommandException


def activate(api, args):
    args_count = len(args)
    if args_count != 1:
        raise CommandException("'activate' takes 1 argument but {} were given".format(args_count))

    title = args[0]
    result = api.brain.search.by_title(title)
    result_len = len(result)
    if result_len == 0:
        raise CommandException("No thoughts found")
    elif result_len > 1:
        raise CommandException("More than one thought found")
    else:
        return [result[0]]


def set_title_or_description(api, args):
    args_count = len(args)
    if args_count == 2:
        title = args[0]
        new_title_or_desc = args[1]
        result = api.brain.search.by_title(title)
        result_len = len(result)
        if result_len == 0:
            raise CommandException("No thoughts found")
        elif result_len > 1:
            raise CommandException("More than one thought found")
        else:
            return [result[0], new_title_or_desc]
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
        try:
            thought = api.storage.get(title)
            return [thought]
        except:
            raise Exception("Unable to delete, because thought '{}' does not exist".format(title))
    elif len(args) == 0:
        if not api.brain.state.active_thought:
            raise Exception("No active thought")
        return [api.brain.state.active_thought]
    else:
        raise Exception("'delete' takes 0 or 1 argument but {} were given".format(len(args)))


def link(api, args):
    if len(args) == 3:
        src_title = args[0]
        dst_title = args[1]
        kind = args[2]
        try:
            src_thought = api.storage.search({
                "field": "definition.title",
                "operator": "=",
                "value": src_title})[0]
            dst_thought = api.storage.search({
                "field": "definition.title",
                "operator": "=",
                "value": dst_title})[0]
            return [src_thought, dst_thought, kind]
        except:
            raise Exception("Unable to link these thoughts")
    #elif len(args) == 1:
    #    title_or_desc = args[0]
    #    if not api.active_thought:
    #        raise Exception("No active thought")
    #    return [api.active_thought, title_or_desc]
    else:
        raise Exception("'title' takes 1 or 2 arguments but {} were given".format(len(args)))