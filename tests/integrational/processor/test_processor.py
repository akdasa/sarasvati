import pytest

from sarasvati.exceptions import CommandException


def test_processor_unknown_command(api):
    cmd = "/un@know@n"
    with pytest.raises(CommandException) as exc:
        api.execute(cmd)
    assert exc.value.args[0] == "Unknown command '{}'".format(cmd)
