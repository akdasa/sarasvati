import pytest

from sarasvati.commands import CommandException


def test_processor_unknown_command(api):
    cmd = "/un@know@n"
    with pytest.raises(CommandException) as exc:
        api.processor.execute(cmd)
    assert exc.value.args[0] == "Unknown command '{}'".format(cmd)