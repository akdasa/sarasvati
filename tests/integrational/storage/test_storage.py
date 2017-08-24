def test_remove_entity_links(api):
    api.execute("/c one key:one")
    api.execute("/c two parent:one key:two")
    api.execute("/d one")
    api.storage.cache.clear()

    thought = api.storage.get("two")
    assert len(thought.links.all) == 0
    assert api.storage.get("one") is None


def test_load_linked_child_and_parent(storage):
    brain = storage.get("Brain")
    tasks = list(filter(lambda x: x.title == "Tasks", brain.links.children))[0]
    tasks_db = storage.get("Tasks")

    assert tasks is tasks_db
    assert tasks in brain.links.children
    assert brain in tasks.links.parents


def test_load_linked_child_parent_and_lazy_child(storage):
    brain = storage.get("Brain")
    cook = storage.get("Task2")
    tasks = storage.get("Tasks")

    assert tasks in brain.links.children
    assert cook in tasks.links.children
    assert brain in tasks.links.parents
    assert tasks in cook.links.parents


def test_cache_linked(storage):
    storage.get("Brain")
    assert storage.cache.is_cached("Brain") is True
    assert storage.cache.is_cached("Tasks") is True
    assert storage.cache.is_cached("Recipes") is True


def test_cache_linked_nearest_not_lazy(storage):
    storage.get("Brain")
    assert storage.cache.is_lazy("Brain") is False
    assert storage.cache.is_lazy("Tasks") is False
    assert storage.cache.is_lazy("Recipes") is False


def test_cache_linked_far_lazy(storage):
    storage.get("Brain")
    assert storage.cache.is_lazy("Task1") is True


def test_cache_linked_far_lazy_2(api):
    api.execute("/c root key:root")
    api.execute("/c child1 parent:root key:child1")
    api.execute("/c child2 parent:child1 key:child2")
    api.storage.cache.clear()

    api.execute("/show root")
    api.execute("/show child1")
    assert api.storage.cache.is_lazy("root") is False
    assert api.storage.cache.is_lazy("child1") is False
    assert api.storage.cache.is_lazy("child2") is False


def test_cache_linked_far_lazy_3(api):
    api.execute("/c root key:root")
    api.execute("/c child1 parent:root key:child1")
    api.execute("/c child2 parent:child1 key:child2")
    api.storage.cache.clear()

    api.execute("/show root")
    assert api.storage.cache.is_lazy("child2") is True


def test_storage_search_contains(api):
    thought = api.execute("/c CaSe SeNsItIvE TiTlE").value
    result = api.utilities.find_one_by_title("eNsItIv", operator="~")
    assert result == thought


def test_storage_search_contains_case(api):
    thought = api.execute("/c CaSe SeNsItIvE TiTlE").value
    result = api.utilities.find_one_by_title("sensitive", operator="~~")
    assert result == thought
