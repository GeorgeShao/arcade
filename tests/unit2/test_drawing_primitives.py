import arcadeplus
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MyGame(arcadeplus.Window):
    """ Main application class. """

    def __init__(self, width, height):
        """
        Initializer
        """
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        new_path = os.path.join(file_path, '..', '..', 'arcadeplus', 'examples')
        os.chdir(new_path)

        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def on_draw(self):
        """
        Render the screen.
        """

        # Start the render process. This must be done before any drawing commands.
        arcadeplus.start_render()

        # Draw a grid
        # Draw vertical lines every 120 pixels
        for x in range(0, 601, 120):
            arcadeplus.draw_line(x, 0, x, 600, arcadeplus.color.BLACK, 2)

        # Draw horizontal lines every 200 pixels
        for y in range(0, 601, 200):
            arcadeplus.draw_line(0, y, 800, y, arcadeplus.color.BLACK, 2)

        # Draw a point
        arcadeplus.draw_text("draw_point", 3, 405, arcadeplus.color.BLACK, 12)
        arcadeplus.draw_point(60, 495, arcadeplus.color.RED, 10)

        # Draw a set of points
        arcadeplus.draw_text("draw_points", 123, 405, arcadeplus.color.BLACK, 12)
        point_list = ((165, 495),
                      (165, 480),
                      (165, 465),
                      (195, 495),
                      (195, 480),
                      (195, 465))
        arcadeplus.draw_points(point_list, arcadeplus.color.ZAFFRE, 10)

        # Draw a line
        arcadeplus.draw_text("draw_line", 243, 405, arcadeplus.color.BLACK, 12)
        arcadeplus.draw_line(270, 495, 300, 450, arcadeplus.color.WOOD_BROWN, 3)

        # Draw a set of lines
        arcadeplus.draw_text("draw_lines", 363, 405, arcadeplus.color.BLACK, 12)
        point_list = ((390, 450),
                      (450, 450),
                      (390, 480),
                      (450, 480),
                      (390, 510),
                      (450, 510)
                      )
        arcadeplus.draw_lines(point_list, arcadeplus.color.BLUE, 3)

        # Draw a line strip
        arcadeplus.draw_text("draw_line_strip", 483, 405, arcadeplus.color.BLACK, 12)
        point_list = ((510, 450),
                      (570, 450),
                      (510, 480),
                      (570, 480),
                      (510, 510),
                      (570, 510)
                      )
        arcadeplus.draw_line_strip(point_list, arcadeplus.color.TROPICAL_RAIN_FOREST, 3)
        arcadeplus.draw_line_strip(point_list, arcadeplus.color.BEIGE)

        # Draw a polygon
        arcadeplus.draw_text("draw_polygon_outline", 3, 207, arcadeplus.color.BLACK, 9)
        point_list = ((30, 240),
                      (45, 240),
                      (60, 255),
                      (60, 285),
                      (45, 300),
                      (30, 300))
        arcadeplus.draw_polygon_outline(point_list, arcadeplus.color.SPANISH_VIOLET, 3)

        # Draw a filled in polygon
        arcadeplus.draw_text("draw_polygon_filled", 123, 207, arcadeplus.color.BLACK, 9)
        point_list = ((150, 240),
                      (165, 240),
                      (180, 255),
                      (180, 285),
                      (165, 300),
                      (150, 300))
        arcadeplus.draw_polygon_filled(point_list, arcadeplus.color.SPANISH_VIOLET)

        # Draw an outline of a circle
        arcadeplus.draw_text("draw_circle_outline", 243, 207, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_circle_outline(300, 285, 18, arcadeplus.color.WISTERIA, 3)
        arcadeplus.draw_circle_outline(350, 285, 18, arcadeplus.color.WISTERIA)

        # Draw a filled in circle
        arcadeplus.draw_text("draw_circle_filled", 363, 207, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_circle_filled(420, 285, 18, arcadeplus.color.GREEN)

        # Draw an ellipse outline, and another one rotated
        arcadeplus.draw_text("draw_ellipse_outline", 483, 207, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_ellipse_outline(540, 273, 15, 36, arcadeplus.color.AMBER, 3)
        arcadeplus.draw_ellipse_outline(540, 336, 15, 36,
                                    arcadeplus.color.BLACK_BEAN, 3, 45)

        # Draw a filled ellipse, and another one rotated
        arcadeplus.draw_text("draw_ellipse_filled", 3, 3, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_ellipse_filled(60, 81, 15, 36, arcadeplus.color.AMBER)
        arcadeplus.draw_ellipse_filled(60, 144, 15, 36,
                                   arcadeplus.color.BLACK_BEAN, 45)

        # Draw an arc, and another one rotated
        arcadeplus.draw_text("draw_arc/filled_arc", 123, 3, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_arc_outline(150, 81, 15, 36,
                                arcadeplus.color.BRIGHT_MAROON, 90, 360)
        arcadeplus.draw_arc_filled(150, 144, 15, 36,
                               arcadeplus.color.BOTTLE_GREEN, 90, 360, 45)

        # Draw an rectangle outline
        arcadeplus.draw_text("draw_rect", 243, 3, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_rectangle_outline(295, 100, 45, 65,
                                      arcadeplus.color.BRITISH_RACING_GREEN)
        arcadeplus.draw_rectangle_outline(295, 160, 20, 45,
                                      arcadeplus.color.BRITISH_RACING_GREEN, 3, 45)

        # Draw a filled in rectangle
        arcadeplus.draw_text("draw_filled_rect", 363, 3, arcadeplus.color.BLACK, 10)
        arcadeplus.draw_rectangle_filled(420, 100, 45, 65, arcadeplus.color.BLUSH)
        arcadeplus.draw_rectangle_filled(420, 160, 20, 40, arcadeplus.color.BLUSH, 45)

        # Load and draw an image to the screen
        # Image from kenney.nl asset pack #1
        arcadeplus.draw_text("draw_bitmap", 483, 3, arcadeplus.color.BLACK, 12)
        texture = arcadeplus.load_texture(":resources:images/space_shooter/playerShip1_orange.png")
        scale = .6
        # arcadeplus.draw_texture_rectangle(540, 120, scale * texture.width,
        #                               scale * texture.height, texture, 0)
        # arcadeplus.draw_texture_rectangle(540, 60, scale * texture.width,
        #                               scale * texture.height, texture, 45)
        #
        # Overlapping, with transparency test
        # Draw
        arcadeplus.draw_rectangle_filled(650, 100, 50, 50, (255, 0, 0))
        arcadeplus.draw_rectangle_filled(670, 100, 50, 50, (0, 255, 0, 127))

        # Test colors
        color = arcadeplus.get_pixel(635, 100)
        assert color == (255, 0, 0)
        color = arcadeplus.get_pixel(670, 100)
        assert color == (128, 127, 0)
        color = arcadeplus.get_pixel(690, 100)
        assert color == (128, 255, 128)

        # Test this other thing
        color = arcadeplus.get_pixel(100, 100)
        assert color == (255, 255, 255)

        # Run the get image. Ideally we'd test the output
        arcadeplus.get_image()


def test_main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.test()
    window.close()
