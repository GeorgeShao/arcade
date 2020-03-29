"""
Example "arcadeplus" library code.

Showing how to do nested loops.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.nested_loops_box
"""

# Library imports
import arcadeplus

COLUMN_SPACING = 20
ROW_SPACING = 20
LEFT_MARGIN = 110
BOTTOM_MARGIN = 110

# Open the window and set the background
arcadeplus.open_window(400, 400, "Complex Loops - Box")

arcadeplus.set_background_color(arcadeplus.color.WHITE)

# Start the render process. This must be done before any drawing commands.
arcadeplus.start_render()

# Loop for each row
for row in range(10):
    # Loop for each column
    for column in range(10):
        # Calculate our location
        x = column * COLUMN_SPACING + LEFT_MARGIN
        y = row * ROW_SPACING + BOTTOM_MARGIN

        # Draw the item
        arcadeplus.draw_circle_filled(x, y, 7, arcadeplus.color.AO)

# Finish the render.
arcadeplus.finish_render()

# Keep the window up until someone closes it.
arcadeplus.run()
