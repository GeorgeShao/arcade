import arcadeplus
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
TITLE = 'arcadeplus cx_Freeze Sample'
BACKGROUND_COLOR = arcadeplus.color.WHITE


def resource_path(file):
    path = 'resources/' + file
    # are we in a frozen environment (e.g. pyInstaller)?
    if getattr(sys, 'frozen', False):
        # noinspection PyProtectedMember,PyUnresolvedReferences
        path = sys._MEIPASS.replace('\\', '/') + '/' + path
    return path


def main():
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    arcadeplus.set_background_color(BACKGROUND_COLOR)
    arcadeplus.start_render()
    arcadeplus.draw_circle_filled(400, 250, 100, arcadeplus.color.BLACK)
    # load image
    image = arcadeplus.load_texture(resource_path('character.png'))
    arcadeplus.draw_texture_rectangle(200, 250, image.width, image.height, image)
    # load sound
    sound = arcadeplus.sound.load_sound(resource_path('cat-meow.wav'))
    arcadeplus.sound.play_sound(sound)
    arcadeplus.finish_render()
    arcadeplus.run()
    return


main()
