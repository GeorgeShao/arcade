import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MyGame(arcadeplus.Window):
    """ Main application class. """

    def __init__(self, width, height):
        """
        Initializer
        """
        super().__init__(width, height)

        arcadeplus.set_background_color(arcadeplus.color.WHITE)
        self.laser_wav = arcadeplus.load_sound(":resources:sounds/laser1.wav")
        self.laser_mp3 = arcadeplus.load_sound(":resources:sounds/laser1.mp3")
        self.laser_ogg = arcadeplus.load_sound(":resources:sounds/laser1.ogg")
        self.frame_count = 0

    def update(self, dt):
        self.frame_count += 1

        if self.frame_count == 1:
            arcadeplus.play_sound(self.laser_wav)

        if self.frame_count == 60:
            arcadeplus.play_sound(self.laser_ogg)

        if self.frame_count == 90:
            arcadeplus.play_sound(self.laser_mp3)

    def on_draw(self):
        """
        Render the screen.
        """

        # Start the render process. This must be done before any drawing commands.
        arcadeplus.start_render()


def test_main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.test(90)
    window.close()
