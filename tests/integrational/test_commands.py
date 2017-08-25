def test_delete_and_revert(api, script):
    script(["/c 1",
            "/c 2 parent:1",
            "/d 2",
            "/r"], clear_cache=True)

    thought = api.execute("/a 1").value
    assert len(thought.links.all) == 1

    thought = api.execute("/a 2").value
    assert len(thought.links.all) == 1
