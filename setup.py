from os import path
import sys
from setuptools import setup

VERSION = 'default'
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

# execute the file
execfile("arcadeplus/version.py", locals=locals())

RELEASE = VERSION

if __name__ == "__main__":

    install_requires = [
        'pyglet',
        'pillow',
        'numpy',
        'pyglet-ffmpeg2',
        'pytiled-parser'
    ]
    if sys.version_info[0] == 3 and sys.version_info[1] == 6:
        install_requires.append('dataclasses')

    fname = path.join(path.dirname(path.abspath(__file__)), "README.rst")
    with open(fname, "r") as f:
        long_desc = f.read()

    setup(
          name="arcadeplus",
          version=RELEASE,
          description="ArcadePlus Graphics Library",
          long_description=long_desc,
          author="George Shao",
          author_email="georgeshao123@gmail.com",
          license="gpl-3.0",
          url="https://github.com/GeorgeShao/arcadeplus",
          download_url="https://github.com/GeorgeShao/arcadeplus/archive/1.0.4.tar.gz",
          install_requires=install_requires,
          packages=["arcadeplus",
                    "arcadeplus.key",
                    "arcadeplus.color",
                    "arcadeplus.csscolor",
                    "arcadeplus.examples"
                    ],
          python_requires='>=3.6',
          classifiers=[
              "Development Status :: 5 - Production/Stable", # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
              "Intended Audience :: Developers",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              "Operating System :: OS Independent",
              "Programming Language :: Python",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "Programming Language :: Python :: 3.8",
              "Programming Language :: Python :: Implementation :: CPython",
              "Topic :: Software Development :: Libraries :: Python Modules",
              ],
          test_suite="tests",
          package_data={'arcadeplus': ['resources/gui_themes/Fantasy/Buttons/*',
                                   'resources/gui_themes/Fantasy/DialogueBox/*',
                                   'resources/gui_themes/Fantasy/Menu/*',
                                   'resources/gui_themes/Fantasy/TextBox/*',
                                   'resources/gui_themes/Fantasy/Window/*',
                                   'resources/images/*',
                                   'resources/images/alien/*',
                                   'resources/images/animated_characters/female_adventurer/*',
                                   'resources/images/animated_characters/female_person/*',
                                   'resources/images/animated_characters/male_adventurer/*',
                                   'resources/images/animated_characters/male_person/*',
                                   'resources/images/animated_characters/robot/*',
                                   'resources/images/animated_characters/zombie/*',
                                   'resources/images/backgrounds/*',
                                   'resources/images/enemies/*',
                                   'resources/images/isometric_dungeon/*',
                                   'resources/images/items/*',
                                   'resources/images/pinball/*',
                                   'resources/images/space_shooter/*',
                                   'resources/images/spritesheets/*',
                                   'resources/images/texture_transform/*',
                                   'resources/images/tiles/*',
                                   'resources/sounds/*',
                                   'resources/tmx_maps/*',
                                   'py.typed']},
         )
