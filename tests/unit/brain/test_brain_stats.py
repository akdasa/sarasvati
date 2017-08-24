from sarasvati.brain import Thought


def test_stats(brain):
    brain.storage.add(Thought())
    assert brain.stats.thoughts_count == 1
