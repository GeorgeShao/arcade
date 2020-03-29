import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Resources"
CHARACTER_SCALING = 1.0


class MyTestWindow(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

        self.sprite = arcadeplus.Sprite(":resources:images/items/coinGold.png", CHARACTER_SCALING)
        self.sprite.center_x = 50
        self.sprite.center_y = 50

        self.sprite_list = arcadeplus.SpriteList()
        self.sprite_list.append(self.sprite)


    def on_draw(self):
        try:
            arcadeplus.start_render()

            assert arcadeplus.get_pixel(50, 50) == (59, 122, 87)
            self.sprite.draw()
            assert arcadeplus.get_pixel(50, 50) == (255, 204, 0)

        except Exception as e:
            assert e is None



def test_sprite():
    window = MyTestWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.test(50)
    window.close()
