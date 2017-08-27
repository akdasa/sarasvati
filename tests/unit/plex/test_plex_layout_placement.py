from plugins.app.gui.plex import PlexLayoutPlacement, PlacementOptions, PlexState


def test_options(thoughts):
    p = PlexLayoutPlacement()
    o = PlacementOptions(width=550, height=550, step=100)
    s = PlexState()
    s.add(thoughts["Root"], "root")
    s.add(thoughts["Child1"], "child")
    s.add(thoughts["Child2"], "child")
    s.add(thoughts["Parent1"], "parent")
    s.add(thoughts["Parent2"], "parent")
    s.add(thoughts["Reference1"], "reference")
    s.add(thoughts["Reference2"], "reference")

    r = p.place(s, o)
    assert r.position(thoughts["Root"]) == [0, 0]
    assert r.position(thoughts["Child1"]) == [-200, 200]
    assert r.position(thoughts["Child2"]) == [200, 200]
    assert r.position(thoughts["Parent1"]) == [-200, -200]
    assert r.position(thoughts["Parent2"]) == [200, -200]
    assert r.position(thoughts["Reference1"]) == [-200, 0]
    assert r.position(thoughts["Reference2"]) == [-200, -100]

