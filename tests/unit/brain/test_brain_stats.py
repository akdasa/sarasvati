from sarasvati.brain import Thought


def test_brain_stats_thought_count(brain):
    brain.storage.add(Thought())
    assert brain.stats.thoughts_count == 1
