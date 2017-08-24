def test_init(component):
    """Init component with name"""
    c = component("My")
    assert c.name == "My"


def test_on_added_called(composite, component):
    """Init component with name"""
    cc = composite()
    ct = component("My")
    cc.add_component(ct)
    assert ct.on_added_called is cc
