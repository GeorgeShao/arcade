import random
import arcadeplus
import os
import timeit
import time
import collections
import pyglet

START_COUNT = 5
STOP_COUNT = 200
SHAPE_INCREMENT = START_COUNT
RESULTS_FILE = "arcadeplus_results.csv"

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "ArcadePlus Shapes Stress Test"
TOP_MARGIN = 40

class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=1000)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)

class Line: 
    def __init__(self):
        self.start_x = random.randrange(SCREEN_WIDTH)
        self.start_y = random.randrange(SCREEN_HEIGHT - TOP_MARGIN)
        self.end_x = random.randrange(SCREEN_WIDTH)
        self.end_y = random.randrange(SCREEN_HEIGHT - TOP_MARGIN)

    def draw(self):
        arcadeplus.draw_line(self.start_x, self.start_y,
                         self.end_x, self.end_y, arcadeplus.color.WOOD_BROWN, 4)


class MyGame(arcadeplus.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.shape_list = []

        self.processing_time = 0
        self.draw_time = 0
        self.program_start_time = timeit.default_timer()
        self.sprite_count_list = []
        self.fps_list = []
        self.processing_time_list = []
        self.drawing_time_list = []
        self.last_fps_reading = 0
        self.fps = FPSCounter()

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

        # Open file to save timings
        self.results_file = open(RESULTS_FILE, "w")

    def add_shapes(self):

        # Create the coins
        for i in range(SHAPE_INCREMENT):
            shape = Line()

            # Add the coin to the lists
            self.shape_list.append(shape)

    def setup(self):
        """ Set up the game and initialize the variables. """

        pass

    def on_draw(self):
        """ Draw everything """

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        arcadeplus.start_render()
        for shape in self.shape_list:
            shape.draw()

        # Display info on sprites
        output = f"Shape count: {len(self.shape_list):,}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 20, arcadeplus.color.BLACK, 16)

        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 40, arcadeplus.color.BLACK, 16)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 60, arcadeplus.color.BLACK, 16)

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 80, arcadeplus.color.BLACK, 16)

        self.draw_time = timeit.default_timer() - draw_start_time
        self.fps.tick()

    def update(self, delta_time):
        # Start update timer
        start_time = timeit.default_timer()

        # self.shape_list.update()

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

        # Total time program has been running
        total_program_time = int(timeit.default_timer() - self.program_start_time)

        # Print out stats, or add more sprites
        if total_program_time > self.last_fps_reading:
            self.last_fps_reading = total_program_time

            # It takes the program a while to "warm up", so the first
            # few seconds our readings will be off. So wait some time
            # before taking readings
            if total_program_time > 5:

                # We want the program to run for a while before taking
                # timing measurements. We don't want the time it takes
                # to add new sprites to be part of that measurement. So
                # make sure we have a clear second of nothing but
                # running the sprites, and not adding the sprites.
                if total_program_time % 2 == 1:

                    # Take timings
                    output = f"{total_program_time}, {len(self.shape_list)}, {self.fps.get_fps():.1f}, " \
                             f"{self.processing_time:.4f}, {self.draw_time:.4f}\n"

                    self.results_file.write(output)
                    print(output, end="")
                    if len(self.shape_list) >= STOP_COUNT:
                        pyglet.app.exit()
                        return

                    self.sprite_count_list.append(len(self.shape_list))
                    self.fps_list.append(round(self.fps.get_fps(), 1))
                    self.processing_time_list.append(self.processing_time)
                    self.drawing_time_list.append(self.draw_time)

                    # Now add the coins
                    self.add_shapes()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == "__main__":
    main()