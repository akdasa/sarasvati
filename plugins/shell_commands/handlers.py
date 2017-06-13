import colored
from colored import stylize

__TITLE_STYLE = colored.fg("green")
__LINK_STYLE = colored.fg("blue") + colored.attr("underlined")
__DESC_STYLE = colored.fg("dark_gray")


def ls(api, args):
    title = args.get("arg")
    search_result = api.brain.search.by_title(title, operator="~~")
    for thought in search_result:
        print(stylize(thought.title, __TITLE_STYLE), thought.description)


def show(api, args):
    title = args.get("arg")
    thought = api.utilities.find_one_by_title(title) if title else api.brain.state.active_thought

    print(stylize(thought.title, __TITLE_STYLE))
    if thought.description:
        print(thought.description)

    links = thought.links.all
    for thought in links:
        link = links[thought]
        print("{}: {} {}".format(link.kind.capitalize(),
                                 stylize(thought.title, __LINK_STYLE),
                                 stylize(thought.description, __DESC_STYLE)))

def quit_(api, args):
    print("Good bye, take care!")
