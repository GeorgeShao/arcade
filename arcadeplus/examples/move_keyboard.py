"""
This simple animation example shows how to move an item with the keyboard.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.move_keyboard
"""

import arcadeplus

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Move Keyboard Example"
MOVEMENT_SPEED = 3


class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius, color):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcadeplus.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self):
        # Move the ball
        self.position_y += self.change_y
        self.position_x += self.change_x

        # See if the ball hit the edge of the screen. If so, change direction
        if self.position_x < self.radius:
            self.position_x = self.radius

        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius

        if self.position_y < self.radius:
            self.position_y = self.radius

        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius


class MyGame(arcadeplus.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        arcadeplus.set_background_color(arcadeplus.color.ASH_GREY)

        # Create our ball
        self.ball = Ball(50, 50, 0, 0, 15, arcadeplus.color.AUBURN)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcadeplus.start_render()
        self.ball.draw()

    def on_update(self, delta_time):
        self.ball.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcadeplus.key.LEFT:
            self.ball.change_x = -MOVEMENT_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.ball.change_x = MOVEMENT_SPEED
        elif key == arcadeplus.key.UP:
            self.ball.change_y = MOVEMENT_SPEED
        elif key == arcadeplus.key.DOWN:
            self.ball.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.ball.change_x = 0
        elif key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.ball.change_y = 0


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == "__main__":
    main()
