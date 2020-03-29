"""
This program shows how to:
  * Display a sequence of screens in your game.  The "arcadeplus.View"
    class makes it easy to separate the code for each screen into
    its own class.
  * This example shows the absolute basics of using "arcadeplus.View".
    See the "different_screens_example.py" for how to handle
    screen-specific data.

Make a separate class for each view (screen) in your game.
The class will inherit from arcadeplus.View. The structure will
look like an arcadeplus.Window as each View will need to have its own draw,
update and window event methods. To switch a View, simply create a View
with `view = MyView()` and then use the "self.window.set_view(view)" method.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.view_screens_minimal
"""

import arcadeplus
import os


WIDTH = 800
HEIGHT = 600


class MenuView(arcadeplus.View):
    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text("Menu Screen - click to advance", WIDTH/2, HEIGHT/2,
                         arcadeplus.color.BLACK, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcadeplus.View):

    def __init__(self):
        super().__init__()
        # Create variables here

    def setup(self):
        # Replace 'pass' with the code to set up your game
        pass

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.ORANGE_PEEL)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text("Game - press SPACE to advance", WIDTH/2, HEIGHT/2,
                         arcadeplus.color.BLACK, font_size=30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)


class GameOverView(arcadeplus.View):
    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text("Game Over - press ESCAPE to advance", WIDTH/2, HEIGHT/2,
                         arcadeplus.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcadeplus.Window(WIDTH, HEIGHT, "Different Views Minimal Example")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcadeplus.run()


if __name__ == "__main__":
    main()
