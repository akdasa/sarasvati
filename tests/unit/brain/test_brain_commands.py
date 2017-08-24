import pytest


def test_execute(brain, command):
    brain.commands.execute(command)
    assert command.executed is True


def test_revert(brain, command):
    brain.commands.execute(command)
    brain.commands.revert()
    assert command.executed is True
    assert command.reverted is True


def test_revert_nothing(brain):
    with pytest.raises(Exception) as ex:
        brain.commands.revert()
    assert ex.value.args[0] == "Nothing to revert"


def test_execute_twice(brain, command):
    brain.commands.execute(command)
    with pytest.raises(Exception) as exc:
        brain.commands.execute(command)
    assert exc.value.args[0] == "Command already executed"


def test_revert_transaction(brain, tri):
    t, c1, c2 = tri
    brain.commands.execute(c1, transaction=t)
    brain.commands.execute(c2, transaction=t)
    brain.commands.revert()
    assert len(brain.commands.history) == 0


def test_revert_different_transaction(brain, tri):
    t, c1, c2 = tri
    brain.commands.execute(c1, transaction=t)
    brain.commands.execute(c2)
    brain.commands.revert()
    assert len(brain.commands.history) == 1
    assert brain.commands.history == [c1]


def test_revert_different_transaction_2(brain, tri):
    t, c1, c2 = tri
    brain.commands.execute(c1)
    brain.commands.execute(c2, transaction=t)
    brain.commands.revert()
    assert len(brain.commands.history) == 1
    assert brain.commands.history == [c1]


def test_can_execute(brain, command):
    command.set_can_execute(False)
    with pytest.raises(Exception) as ex:
        brain.commands.execute(command)
    assert ex.value.args[0] == "Command can not be executed"
