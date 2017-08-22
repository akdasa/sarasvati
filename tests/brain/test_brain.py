import pytest

from sarasvati.commands import Transaction


def test_brain_init(brain):
    assert brain.commands is not None
    assert brain.search is not None
    assert brain.stats is not None
    assert brain.state is not None
    assert brain.storage is not None


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


def test_brain_revert_command_with_transaction(brain, command, command2):
    t = Transaction()
    brain.commands.execute(command, transaction=t)
    brain.commands.execute(command2, transaction=t)
    brain.commands.revert()
    assert len(brain.commands.history) == 0


def test_brain_revert_command_with_different_transaction(brain, command, command2):
    t = Transaction()
    brain.commands.execute(command, transaction=t)
    brain.commands.execute(command2)
    brain.commands.revert()
    assert len(brain.commands.history) == 1
    assert brain.commands.history == [command]


def test_brain_revert_command_with_different_transaction_2(brain, command, command2):
    t = Transaction()
    brain.commands.execute(command)
    brain.commands.execute(command2, transaction=t)
    brain.commands.revert()
    assert len(brain.commands.history) == 1
    assert brain.commands.history == [command]
