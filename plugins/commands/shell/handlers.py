import colored
from colored import stylize

from sarasvati.commands import CommandException

__TITLE_STYLE = colored.fg("green")
__LINK_STYLE = colored.fg("blue") + colored.attr("underlined")
__DESC_STYLE = colored.fg("dark_gray")
__SHORTCUT_STYLE = colored.fg("cyan")


def ls(api, args):
    title = args.get("arg")
    search_result = api.brain.search.by_title(title, operator="~~")
    shortcut_id = 0
    api.brain.state.shortcuts.clear()
    for thought in search_result:
        api.brain.state.shortcuts.set(shortcut_id, thought)
        print(
            stylize(shortcut_id, __SHORTCUT_STYLE),
            stylize(thought.title, __TITLE_STYLE),
            thought.description)
        shortcut_id += 1


def show(api, args):
    title = args.get("arg")
    thought = api.utilities.find_one_by_title(title) if title else api.brain.state.active_thought

    if not thought:
        raise CommandException("Nothing to show")

    print(stylize(thought.title, __TITLE_STYLE))
    if thought.description:
        print(thought.description)

    shortcut_id = 0
    api.brain.state.shortcuts.clear()
    links = thought.links.all
    for thought in links:
        api.brain.state.shortcuts.set(shortcut_id, thought)
        link = links[thought]
        print("{} {}: {} {}".format(stylize(shortcut_id, __SHORTCUT_STYLE),
                                    link.kind.capitalize(),
                                    stylize(thought.title, __LINK_STYLE),
                                    stylize(thought.description, __DESC_STYLE)))
        shortcut_id += 1


# noinspection PyUnusedLocal
def show_shortcuts(api, args):
    shortcuts = api.brain.state.shortcuts.all
    for s in shortcuts:
        v = shortcuts[s]
        print(stylize(s, __SHORTCUT_STYLE), stylize(v.title, __TITLE_STYLE))


# noinspection PyUnusedLocal
def quit_(api, args):
    print("Good bye, take care!")
