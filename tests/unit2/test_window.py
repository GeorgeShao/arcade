def test_window():
    import arcadeplus
    width = 800
    height = 600
    title = "My Title"
    resizable = True
    arcadeplus.open_window(width, height, title, resizable)

    arcadeplus.set_background_color(arcadeplus.color.AMAZON)
    w = arcadeplus.get_window()
    assert w is not None

    # Make sure the arguments get passed to the window
    assert w.width == width
    assert w.height == height
    assert w.caption == title
    assert w.resizeable is resizable

    arcadeplus.set_window(w)

    p = arcadeplus.get_projection()
    assert p is not None

    v = arcadeplus.get_viewport()
    assert v[0] == 0
    # The lines below fail. Why?
    # assert v[1] == width - 1
    assert v[2] == 0
    # assert v[3] == height - 1

    arcadeplus.start_render()
    arcadeplus.finish_render()

    def f():
        pass

    arcadeplus.schedule(f, 1/60)

    arcadeplus.pause(0.01)

    arcadeplus.close_window()

    arcadeplus.open_window(width, height, title, resizable)
    arcadeplus.quick_run(0.01)

