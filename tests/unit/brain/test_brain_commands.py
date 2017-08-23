import pytest

from sarasvati.commands import Transaction, Command


def test_brain_execute_command(brain):
    command = DummyCommand()
    brain.commands.execute(command)
    assert command.executed is True


def test_brain_undo_command(brain):
    command = DummyCommand()
    brain.commands.execute(command)
    brain.commands.revert()
    assert command.executed is True
    assert command.reverted is True


def test_brain_empty_undo(brain):
    with pytest.raises(Exception) as ex:
        brain.commands.revert()
    assert ex.value.args[0] == "Nothing to revert"


def test_brain_cannot_execute_command_twice(brain):
    command = DummyCommand()
    brain.commands.execute(command)
    with pytest.raises(Exception) as exc:
        brain.commands.execute(command)
    assert exc.value.args[0] == "Command already executed"


def test_brain_revert_command_with_transaction(brain, tri):
    t, c1, c2 = tri
    brain.commands.execute(c1, transaction=t)
    brain.commands.execute(c2, transaction=t)
    brain.commands.revert()
    assert len(brain.commands.history) == 0


def test_brain_revert_command_with_different_transaction(brain, tri):
    t, c1, c2 = tri
    brain.commands.execute(c1, transaction=t)
    brain.commands.execute(c2)
    brain.commands.revert()
    assert len(brain.commands.history) == 1
    assert brain.commands.history == [c1]


def test_brain_revert_command_with_different_transaction_2(brain, tri):
    t, c1, c2 = tri
    brain.commands.execute(c1)
    brain.commands.execute(c2, transaction=t)
    brain.commands.revert()
    assert len(brain.commands.history) == 1
    assert brain.commands.history == [c1]


def test_brain_command_can_execute_false_raises_exception(brain):
    c = DummyCommand(can_execute=False)
    with pytest.raises(Exception) as ex:
        brain.commands.execute(c)
    assert ex.value.args[0] == "Command can not be executed"


# Tests configuration

@pytest.fixture(name="tri")
def __tri():
    return Transaction(), DummyCommand(), DummyCommand()


class DummyCommand(Command):
    def __init__(self, can_execute=True):
        super().__init__()
        self.executed = False
        self.reverted = False
        self.__can_execute = can_execute

    def execute(self):
        self.executed = True

    def revert(self):
        self.reverted = True

    def can_execute(self):
        return self.__can_execute