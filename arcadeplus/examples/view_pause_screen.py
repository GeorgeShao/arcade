"""
This program shows how to have a pause screen without resetting the game.

Make a separate class for each view (screen) in your game.
The class will inherit from arcadeplus.View. The structure will
look like an arcadeplus.Window as each View will need to have its own draw,
update and window event methods. To switch a View, simply create a view
with `view = MyView()` and then use the "self.window.set_view(view)" method.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.view_pause_screen
"""

import arcadeplus
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5


class MenuView(arcadeplus.View):
    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text("Menu Screen", WIDTH/2, HEIGHT/2,
                         arcadeplus.color.BLACK, font_size=50, anchor_x="center")
        arcadeplus.draw_text("Click to advance.", WIDTH/2, HEIGHT/2-75,
                         arcadeplus.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView()
        self.window.show_view(game)


class GameView(arcadeplus.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = arcadeplus.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        arcadeplus.start_render()
        # Draw all the sprites.
        self.player_sprite.draw()

        # Show tip to pause screen
        arcadeplus.draw_text("Press Esc. to pause",
                         WIDTH/2,
                         HEIGHT-100,
                         arcadeplus.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_update(self, delta_time):
        # Call update on all sprites
        self.player_sprite.update()

        # Bounce off the edges
        if self.player_sprite.left < 0 or self.player_sprite.right > WIDTH:
            self.player_sprite.change_x *= -1
        if self.player_sprite.bottom < 0 or self.player_sprite.top > HEIGHT:
            self.player_sprite.change_y *= -1

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)


class PauseView(arcadeplus.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.ORANGE)

    def on_draw(self):
        arcadeplus.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcadeplus.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcadeplus.color.ORANGE + (200,))

        arcadeplus.draw_text("PAUSED", WIDTH/2, HEIGHT/2+50,
                         arcadeplus.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcadeplus.draw_text("Press Esc. to return",
                         WIDTH/2,
                         HEIGHT/2,
                         arcadeplus.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcadeplus.draw_text("Press Enter to reset",
                         WIDTH/2,
                         HEIGHT/2-30,
                         arcadeplus.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcadeplus.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)


def main():
    window = arcadeplus.Window(WIDTH, HEIGHT, "Instruction and Game Over Views Example")
    menu = MenuView()
    window.show_view(menu)
    arcadeplus.run()


if __name__ == "__main__":
    main()
