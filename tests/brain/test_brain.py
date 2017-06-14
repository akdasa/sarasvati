import pytest


def test_brain_commands_accessible(brain):
    assert brain.commands is not None


def test_brain_search_accessible(brain):
    assert brain.search is not None


def test_brain_stats_accessible(brain):
    assert brain.stats is not None


def test_brain_execute_command(brain, command):
    brain.commands.execute(command)
    assert command.executed is True


def test_brain_undo_command(brain, command):
    brain.commands.execute(command)
    brain.commands.revert()
    assert command.executed is True
    assert command.reverted is True


def test_brain_empty_undo(brain):
    with pytest.raises(Exception) as ex:
        brain.commands.revert()
    assert ex.value.args[0] == "Nothing to revert"


def test_brain_cannot_execute_command_twice(brain, command):
    brain.commands.execute(command)
    with pytest.raises(Exception) as exc:
        brain.commands.execute(command)
    assert exc.value.args[0] == "Command already executed"
