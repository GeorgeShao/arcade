"""
Simple program showing how to use a shape list to create a more complex shape
out of basic ones.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.shape_list_demo_person
"""
import arcadeplus

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shape List Demo Person"


def make_person(head_radius,
                chest_height,
                chest_width,
                leg_width,
                leg_height,
                arm_width,
                arm_length,
                arm_gap,
                shoulder_height):

    shape_list = arcadeplus.ShapeElementList()

    # Head
    shape = arcadeplus.create_ellipse_filled(0, chest_height / 2 + head_radius, head_radius, head_radius,
                                         arcadeplus.color.WHITE)
    shape_list.append(shape)

    # Chest
    shape = arcadeplus.create_rectangle_filled(0, 0, chest_width, chest_height, arcadeplus.color.BLACK)
    shape_list.append(shape)

    # Left leg
    shape = arcadeplus.create_rectangle_filled(-(chest_width / 2) + leg_width / 2, -(chest_height / 2) - leg_height / 2,
                                           leg_width, leg_height, arcadeplus.color.RED)
    shape_list.append(shape)

    # Right leg
    shape = arcadeplus.create_rectangle_filled((chest_width / 2) - leg_width / 2, -(chest_height / 2) - leg_height / 2,
                                           leg_width, leg_height, arcadeplus.color.RED)
    shape_list.append(shape)

    # Left arm
    shape = arcadeplus.create_rectangle_filled(-(chest_width / 2) - arm_width / 2 - arm_gap,
                                           (chest_height / 2) - arm_length / 2 - shoulder_height, arm_width, arm_length,
                                           arcadeplus.color.BLUE)
    shape_list.append(shape)

    # Left shoulder
    shape = arcadeplus.create_rectangle_filled(-(chest_width / 2) - (arm_gap + arm_width) / 2,
                                           (chest_height / 2) - shoulder_height / 2, arm_gap + arm_width,
                                           shoulder_height, arcadeplus.color.BLUE_BELL)
    shape_list.append(shape)

    # Right arm
    shape = arcadeplus.create_rectangle_filled((chest_width / 2) + arm_width / 2 + arm_gap,
                                           (chest_height / 2) - arm_length / 2 - shoulder_height, arm_width, arm_length,
                                           arcadeplus.color.BLUE)
    shape_list.append(shape)

    # Right shoulder
    shape = arcadeplus.create_rectangle_filled((chest_width / 2) + (arm_gap + arm_width) / 2,
                                           (chest_height / 2) - shoulder_height / 2, arm_gap + arm_width,
                                           shoulder_height, arcadeplus.color.BLUE_BELL)
    shape_list.append(shape)

    return shape_list


class MyGame(arcadeplus.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        head_radius = 30
        chest_height = 110
        chest_width = 70
        leg_width = 20
        leg_height = 80
        arm_width = 15
        arm_length = 70
        arm_gap = 10
        shoulder_height = 15

        self.shape_list = make_person(head_radius,
                                      chest_height,
                                      chest_width,
                                      leg_width,
                                      leg_height,
                                      arm_width,
                                      arm_length,
                                      arm_gap,
                                      shoulder_height)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):

        """ Set up the game and initialize the variables. """

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcadeplus.start_render()

        self.shape_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.shape_list.center_x += 1
        self.shape_list.center_y += 1
        self.shape_list.angle += .1


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == "__main__":
    main()
