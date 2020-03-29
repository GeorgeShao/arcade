"""
This animation example shows how perform a radar sweep animation.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.radar_sweep
"""

import arcadeplus
import math

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Radar Sweep Example"

# These constants control the particulars about the radar
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250


def on_draw(_delta_time):
    """ Use this function to draw everything to the screen. """

    # Move the angle of the sweep.
    on_draw.angle += RADIANS_PER_FRAME

    # Calculate the end point of our radar sweep. Using math.
    x = SWEEP_LENGTH * math.sin(on_draw.angle) + CENTER_X
    y = SWEEP_LENGTH * math.cos(on_draw.angle) + CENTER_Y

    # Start the render. This must happen before any drawing
    # commands. We do NOT need an stop render command.
    arcadeplus.start_render()

    # Draw the radar line
    arcadeplus.draw_line(CENTER_X, CENTER_Y, x, y, arcadeplus.color.OLIVE, 4)

    # Draw the outline of the radar
    arcadeplus.draw_circle_outline(CENTER_X, CENTER_Y, SWEEP_LENGTH,
                               arcadeplus.color.DARK_GREEN, 10)


# This is a function-specific variable. Before we
# use them in our function, we need to give them initial
# values.
on_draw.angle = 0  # type: ignore # dynamic attribute on function obj


def main():

    # Open up our window
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.set_background_color(arcadeplus.color.BLACK)

    # Tell the computer to call the draw command at the specified interval.
    arcadeplus.schedule(on_draw, 1 / 80)

    # Run the program
    arcadeplus.run()

    # When done running the program, close the window.
    arcadeplus.close_window()


if __name__ == "__main__":
    main()
