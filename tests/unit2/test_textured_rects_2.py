import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Resources"


class MyTestWindow(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

        self.texture = arcadeplus.load_texture(":resources:images/items/coinGold.png")


    def on_draw(self):
        try:
            arcadeplus.start_render()

            x = 50
            y = 50
            scale = 1.0

            assert arcadeplus.get_pixel(50, 50) == (59, 122, 87)
            arcadeplus.draw_scaled_texture_rectangle(x, y, self.texture, scale)
            assert arcadeplus.get_pixel(50, 50) == (255, 204, 0)


        except Exception as e:
            assert e is None


def test_sprite():
    window = MyTestWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.test(50)
    window.close()
