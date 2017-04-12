def activate_map(api, args):
    if len(args) != 1:
        raise Exception("'activate' takes 1 argument but {} were given".format(len(args)))

    title = args[0]
    try:
        thought = api.storage.get(title)
        return [thought]
    except:
        raise Exception("Unable to activate '{}' thought, because it does not exist".format(title))


def set_title_or_description_map(api, args):
    if len(args) == 2:
        title = args[0]
        new_title_or_desc = args[1]
        try:
            thought = api.storage.get(title)
            return [thought, new_title_or_desc]
        except:
            raise Exception("Unable to set, because thought '{}' does not exist".format(title))
    elif len(args) == 1:
        title_or_desc = args[0]
        if not api.active_thought:
            raise Exception("No active thought")
        return [api.active_thought, title_or_desc]
    else:
        raise Exception("'title' takes 1 or 2 arguments but {} were given".format(len(args)))


def delete_map(api, args):
    if len(args) == 1:
        title = args[0]
        try:
            thought = api.storage.get(title)
            return [thought]
        except:
            raise Exception("Unable to delete, because thought '{}' does not exist".format(title))
    elif len(args) == 0:
        if not api.active_thought:
            raise Exception("No active thought")
        return [api.active_thought]
    else:
        raise Exception("'delete' takes 0 or 1 argument but {} were given".format(len(args)))


def link_map(api, args):
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