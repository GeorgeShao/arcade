"""
Show how to have enemies shoot bullets at random intervals.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_bullets_random
"""
import arcadeplus
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites and Random Bullets Example"


class MyGame(arcadeplus.Window):
    """ Main application class """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcadeplus.set_background_color(arcadeplus.color.BLACK)

        self.frame_count = 0
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None

        self.player = None

    def setup(self):
        self.player_list = arcadeplus.SpriteList()
        self.enemy_list = arcadeplus.SpriteList()
        self.bullet_list = arcadeplus.SpriteList()

        # Add player ship
        self.player = arcadeplus.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = arcadeplus.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcadeplus.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

    def on_draw(self):
        """Render the screen. """

        arcadeplus.start_render()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # Have a random 1 in 200 change of shooting each frame
            if random.randrange(200) == 0:
                bullet = arcadeplus.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = -2
                self.bullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = 20


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == "__main__":
    main()
