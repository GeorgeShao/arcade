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

        self.character_list = arcadeplus.SpriteList()
        self.character_sprite = arcadeplus.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", CHARACTER_SCALING)
        self.character_sprite.center_x = 150
        self.character_sprite.center_y = 150
        self.character_list.append(self.character_sprite)

    def on_draw(self):
        arcadeplus.start_render()
        self.character_list.draw()

    def update(self, delta_time):
        self.character_sprite.scale += 0.1


def test_sprite():
    window = MyTestWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Test Text")
    window.test()
    window.close()
