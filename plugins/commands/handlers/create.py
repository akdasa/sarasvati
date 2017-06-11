from plugins.commands.commands import SetDescriptionCommand, LinkCommand, CreateCommand
from sarasvati.commands import CommandException


def create(api, args):
    # /create Thought title desc:some description parent:My Brain as:child
    title = args.get("arg")
    desc = args.get("desc")
    parent = args.get("parent")
    as_ = args.get("as")
    active = api.brain.state.active_thought
    pt = None

    # validation
    if not title:
        raise CommandException("No title specified")
    if parent and as_:
        raise CommandException("'parent' and 'as' arguments cannot be used simultaneously")
    if as_ and not active:
        raise CommandException("'as' argument can be used only with activated thought")
    if as_ and (as_ not in ["child", "parent", "reference"]):
        raise CommandException("Wrong link type in 'as' argument")

    # gather required
    if parent:
        pt = api.utilities.find_one_by_title(parent, "parent")

    # create thought using title specified
    thought = api.execute(CreateCommand(title))
    result = "Thought '{}' created".format(title)

    if desc:  # set description
        api.execute(SetDescriptionCommand(thought, desc))

    if parent:  # link with parent specified
        api.execute(LinkCommand(thought, pt, "parent"))
        result = "Thought '{}' created as parent of '{}'".format(title, pt.title)

    if as_ and active:  # link with active link
        api.execute(LinkCommand(active, thought, as_))
        result = "Thought '{}' created as {} of '{}'".format(title, as_, active.title)

    return result
