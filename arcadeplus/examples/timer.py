"""
Show a timer on-screen.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.timer
"""

import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Timer Example"


class MyGame(arcadeplus.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.total_time = 0.0

    def setup(self):
        """
        Set up the application.
        """
        arcadeplus.set_background_color(arcadeplus.color.WHITE)
        self.total_time = 0.0

    def on_draw(self):
        """ Use this function to draw everything to the screen. """

        # Start the render. This must happen before any drawing
        # commands. We do NOT need an stop render command.
        arcadeplus.start_render()

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcadeplus.draw_text(output, 300, 300, arcadeplus.color.BLACK, 30)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        self.total_time += delta_time


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == "__main__":
    main()
