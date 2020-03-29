"""
Sound Demo

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sound
"""
import arcadeplus
import os

# Set the working directory (where we expect to find files) to the same
# directory this .py file is in. You can leave this out of your own
# code, but it is needed to easily run the examples using "python -m"
# as mentioned at the top of this program.
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

arcadeplus.open_window(300, 300, "Sound Demo")
laser_sound = arcadeplus.load_sound(":resources:sounds/laser1.wav")
arcadeplus.play_sound(laser_sound)
arcadeplus.run()
