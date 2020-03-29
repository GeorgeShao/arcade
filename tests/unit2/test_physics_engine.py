import arcadeplus
import os

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
        self.character_sprite.center_x = 250
        self.character_sprite.center_y = 250
        self.character_sprite.change_x = 5
        self.character_sprite.change_y = 5
        self.character_list.append(self.character_sprite)

        self.wall_list = arcadeplus.SpriteList()

        sprite = arcadeplus.Sprite(":resources:images/tiles/boxCrate_double.png", CHARACTER_SCALING)
        sprite.position = (330, 330)
        sprite.angle = 90
        self.wall_list.append(sprite)

        sprite = arcadeplus.Sprite(":resources:images/tiles/boxCrate_double.png", CHARACTER_SCALING)
        sprite.position = (170, 170)
        sprite.angle = 45
        self.wall_list.append(sprite)

        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.character_sprite, self.wall_list)

    def on_draw(self):
        arcadeplus.start_render()
        self.wall_list.draw()
        self.character_list.draw()

    def update(self, delta_time):
        self.physics_engine.update()

    def switch(self):
        self.character_sprite.change_x = -5
        self.character_sprite.change_y = -5


def test_main():
    window = MyTestWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Test Text")
    window.test(10)
    window.switch()
    window.test(20)
    window.close()
