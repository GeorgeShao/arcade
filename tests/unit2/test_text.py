import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LINE_HEIGHT = 20


class MyTestWindow(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        arcadeplus.start_render()
        current_x = 20

        # First line
        current_y = SCREEN_HEIGHT - LINE_HEIGHT
        arcadeplus.draw_text("Test Text", current_x, current_y, arcadeplus.color.BLACK, 12)

        # Again to test caching
        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text", current_x, current_y, arcadeplus.color.BLACK, 12)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text Anchor Left", SCREEN_WIDTH // 2, current_y,
                         arcadeplus.color.BLACK, 12, anchor_x="left")
        arcadeplus.draw_point(SCREEN_WIDTH // 2, current_y, arcadeplus.color.RED, 5)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text Anchor Center", SCREEN_WIDTH // 2, current_y,
                         arcadeplus.color.BLACK, 12, anchor_x="center")
        arcadeplus.draw_point(SCREEN_WIDTH // 2, current_y, arcadeplus.color.RED, 5)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text Anchor Right", SCREEN_WIDTH // 2, current_y,
                         arcadeplus.color.BLACK, 12, anchor_x="right")
        arcadeplus.draw_point(SCREEN_WIDTH // 2, current_y, arcadeplus.color.RED, 5)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text Anchor Top", SCREEN_WIDTH // 2, current_y,
                         arcadeplus.color.BLACK, 12, anchor_y="top")
        arcadeplus.draw_point(SCREEN_WIDTH // 2, current_y, arcadeplus.color.RED, 5)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text Anchor Center", SCREEN_WIDTH // 2, current_y,
                         arcadeplus.color.BLACK, 12, anchor_y="center")
        arcadeplus.draw_point(SCREEN_WIDTH // 2, current_y, arcadeplus.color.RED, 5)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text("Test Text Anchor Bottom", SCREEN_WIDTH // 2, current_y,
                         arcadeplus.color.BLACK, 12, anchor_y="bottom")
        arcadeplus.draw_point(SCREEN_WIDTH // 2, current_y, arcadeplus.color.RED, 5)

        field_width = SCREEN_WIDTH
        current_y -= LINE_HEIGHT
        arcadeplus.draw_text(f"Test Text Field Width {field_width}", current_x, current_y,
                         arcadeplus.color.BLACK, 12, font_name="arial", width=field_width)

        current_y -= LINE_HEIGHT
        arcadeplus.draw_text(f"Centered Test Text Field Width {field_width}", current_x, current_y,
                         arcadeplus.color.BLACK, 12, font_name="arial", width=field_width, align="center")

        current_y -= LINE_HEIGHT
        font_name = "comic"
        arcadeplus.draw_text("Different font", current_x, current_y, arcadeplus.color.BLACK, 12, font_name=font_name)

        current_y -= LINE_HEIGHT
        # noinspection PyDeprecation
        text = arcadeplus.create_text("Create text", arcadeplus.color.BLACK)
        # noinspection PyDeprecation
        arcadeplus.render_text(text, current_x, current_y)


def test_main():
    window = MyTestWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Test Text")
    window.test()
    window.close()
