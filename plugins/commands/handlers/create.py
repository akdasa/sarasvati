from plugins.commands.commands import SetDescriptionCommand, LinkCommand, CreateCommand
from sarasvati.commands import CommandException

__NOTHING_ERR = "No thought '{}' found to link with."
__AMBIGUOUS_ERR = "Multiple thoughts ({}) found. Unable to link."


def create(api, args):
    # /create Thought title desc:some description parent:My Brain as:child
    title = args.get("arg")
    description = args.get("desc")
    parent = args.get("parent")
    as_ = args.get("as")
    thought = None

    # validation
    if not title:
        raise CommandException("No title specified")
    if parent and as_:
        raise CommandException("'parent' and 'as' arguments cannot be used simultaneously")

    if title:  # create thought using title specified
        thought = api.brain.commands.execute(CreateCommand(title))

    if description:  # set description
        api.brain.commands.execute(SetDescriptionCommand(thought, description))

    if parent:  # link with parent specified
        search_result = api.brain.search.by_title(parent)
        pt = api.get_one(search_result,
                         __NOTHING_ERR.format(parent),
                         __AMBIGUOUS_ERR.format(parent))
        api.brain.commands.execute(LinkCommand(thought, pt, "parent"))

    if as_:  # link with active link
        if api.brain.state.active_thought is None:
            raise CommandException("'as' can be used only with activated thought")

        api.brain.commands.execute(LinkCommand(api.brain.state.active_thought, thought, as_))

