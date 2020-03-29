"""
Drawing an example happy face

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.happy_face
"""

import arcadeplus

# Set constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Happy Face Example"

# Open the window. Set the window title and dimensions
arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Set the background color
arcadeplus.set_background_color(arcadeplus.color.WHITE)

# Clear screen and start render process
arcadeplus.start_render()

# --- Drawing Commands Will Go Here ---

# Draw the face
x = 300
y = 300
radius = 200
arcadeplus.draw_circle_filled(x, y, radius, arcadeplus.color.YELLOW)

# Draw the right eye
x = 370
y = 350
radius = 20
arcadeplus.draw_circle_filled(x, y, radius, arcadeplus.color.BLACK)

# Draw the left eye
x = 230
y = 350
radius = 20
arcadeplus.draw_circle_filled(x, y, radius, arcadeplus.color.BLACK)

# Draw the smile
x = 300
y = 280
width = 120
height = 100
start_angle = 190
end_angle = 350
arcadeplus.draw_arc_outline(x, y, width, height, arcadeplus.color.BLACK,
                        start_angle, end_angle, 10)

# Finish drawing and display the result
arcadeplus.finish_render()

# Keep the window open until the user hits the 'close' button
arcadeplus.run()
