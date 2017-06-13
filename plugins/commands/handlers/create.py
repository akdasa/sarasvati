from plugins.commands.commands import SetDescriptionCommand, LinkCommand, CreateCommand
from plugins.processor.processor import CommandResult
from sarasvati.commands import CommandException


def create(api, args):
    # /create Thought title desc:some description parent:My Brain as:child
    title = args.get("arg") or args.get("title")
    desc = args.get("desc")
    parent = args.get("parent")
    as_ = args.get("as")
    key = args.get("key")
    active = api.brain.state.active_thought

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
    pt = api.utilities.find_one_by_title(parent, "parent") if parent else None

    # create thought using title specified
    thought = api.execute(CreateCommand(title, key=key))
    message = "Thought '{}' created".format(title)

    if desc:  # set description
        api.execute(SetDescriptionCommand(thought, desc))

    if parent:  # link with parent specified
        api.execute(LinkCommand(thought, pt, "parent"))
        message = "Thought '{}' created as child of '{}'".format(title, pt.title)
    elif as_ and active:  # link with active link
        api.execute(LinkCommand(active, thought, as_))
        message = "Thought '{}' created as {} of '{}'".format(title, as_, active.title)

    api.brain.state.shortcuts.set("c", thought)
    return CommandResult(value=thought, message=message)

