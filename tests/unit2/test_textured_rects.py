"""
Tests for textures.
"""
import os
import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LINE_HEIGHT = 20
CHARACTER_SCALING = 0.5


class MyTestWindow(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

        self.texture = arcadeplus.load_texture(":resources:images/space_shooter/playerShip1_orange.png")

    def on_draw(self):
        arcadeplus.start_render()

        scale = .6
        arcadeplus.draw_texture_rectangle(540, 120,
                                      self.texture.image.width * scale,
                                      self.texture.image.height * scale,
                                      self.texture, angle=45)

        arcadeplus.draw_lrwh_rectangle_textured(10, 400, 64, 64, self.texture)

        for i in range(15):
            arcadeplus.draw_scaled_texture_rectangle(i * 50 + 20, 220,
                                                 self.texture,
                                                 scale,
                                                 angle=45, alpha=i * 15)


def test_textured_rects():
    window = MyTestWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Test Textures")
    window.test()
    window.close()
    arcadeplus.cleanup_texture_cache()
