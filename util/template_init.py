"""
The ArcadePLus Library

A simple, easy to use Python module for creating 2D games.
"""

# Note: DO NOT EDIT arcadeplus/__init__.py
# Instead look at util/init_template.py and update_init.py

# Error out if we import arcadeplus with an incompatible version of Python.
import sys

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 6):
    sys.exit("The ArcadePlus Library requires Python 3.6 or higher.")

try:
    import pyglet_ffmpeg2
except Exception as e:
    print("Unable to load the ffmpeg library. ", e)

# noinspection PyPep8
import pyglet

pyglet.options['shadow_window'] = False

# noinspection PyPep8
from arcadeplus import color
# noinspection PyPep8
from arcadeplus import csscolor
# noinspection PyPep8
from arcadeplus import key
# noinspection PyPep8
from arcadeplus import resources
