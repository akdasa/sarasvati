def show_command_map(api, args):
    if len(args) == 1:
        title = args[0]
        try:
            thought = api.database.get(title)
            return [thought]
        except:
            raise Exception("Unable to show '{}' thought, because it does not exist".format(title))
    elif len(args) == 0:
        if not api.active_thought:
            raise Exception("No active thought")
        return [api.active_thought]
    else:
        raise Exception("'show' takes 0 or 1 argument but {} were given".format(len(args)))