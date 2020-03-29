"""
Move Sprite with Joystick

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_move_joystick
"""

import arcadeplus
import os

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite with Joystick Example"

MOVEMENT_SPEED = 5
DEAD_ZONE = 0.05


class Player(arcadeplus.Sprite):

    def __init__(self, filename, scale):
        super().__init__(filename, scale)

        joysticks = arcadeplus.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
        else:
            print("There are no Joysticks")
            self.joystick = None

    def update(self):
        if self.joystick:
            self.change_x = self.joystick.x * MOVEMENT_SPEED
            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.change_x) < DEAD_ZONE:
                self.change_x = 0

            self.change_y = -self.joystick.y * MOVEMENT_SPEED
            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.change_y) < DEAD_ZONE:
                self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcadeplus.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.all_sprites_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcadeplus.SpriteList()

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcadeplus.start_render()

        # Draw all the sprites.
        self.all_sprites_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.all_sprites_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcadeplus.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == "__main__":
    main()
