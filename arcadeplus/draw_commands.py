"""
Drawing commands, some which use vertex buffer objects (VBOs), some which don't.

This module contains commands for basic graphics drawing commands,
but uses Vertex Buffer Objects. This keeps the vertices loaded on
the graphics card for much faster render times.

This module also contains commands for basic graphics drawing commands
that don't use Vertex Buffer Objects
for those primitives/shapes which cannot be easily VBO-optimized.
"""

import math
import array
import itertools
from collections import defaultdict
import pyglet.gl as gl
import numpy as np

import PIL.Image
import PIL.ImageOps
import PIL.ImageDraw

import pyglet.gl as gl

from typing import List, Iterable, Sequence
from typing import Tuple
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Generic
from typing import cast

from arcadeplus import get_projection
from arcadeplus import Color
from arcadeplus import Point, PointList
from arcadeplus import shader
from arcadeplus import earclip
from arcadeplus import rotate_point
from arcadeplus import get_four_byte_color
from arcadeplus import get_points_for_thick_line
from arcadeplus import Texture
from arcadeplus import get_window

if TYPE_CHECKING:  # import for mypy only
    from arcadeplus.arcade_types import Point

_line_vertex_shader = '''
    #version 330
    uniform mat4 Projection;
    in vec2 in_vert;
    in vec4 in_color;
    out vec4 v_color;
    void main() {
       gl_Position = Projection * vec4(in_vert, 0.0, 1.0);
       v_color = in_color;
    }
'''

_line_fragment_shader = '''
    #version 330
    in vec4 v_color;
    out vec4 f_color;
    void main() {
        f_color = v_color;
    }
'''

buffered_shapes = dict()


class Shape:
    def __init__(self):
        self.vao = None
        self.vbo = None
        self.program = None
        self.mode = None
        self.line_width = 1

    def draw(self):
        # program['Projection'].write(get_projection().tobytes())

        with self.vao:
            # assert(self.line_width == 1)
            gl.glLineWidth(self.line_width)

            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glEnable(gl.GL_LINE_SMOOTH)
            gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
            gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
            gl.glEnable(gl.GL_PRIMITIVE_RESTART)
            gl.glPrimitiveRestartIndex(2 ** 32 - 1)

            self.vao.render(mode=self.mode)


TShape = TypeVar('TShape', bound=Shape)
class ShapeElementList(Generic[TShape]):
    """
    A program can put multiple drawing primitives in a ShapeElementList, and then
    move and draw them as one. Do this when you want to create a more complex object
    out of simpler primitives. This also speeds rendering as all objects are drawn
    in one operation.
    """
    def __init__(self):
        """
        Initialize the sprite list
        """
        # List of sprites in the sprite list
        self.shape_list = []
        self.change_x = 0
        self.change_y = 0
        self._center_x = 0
        self._center_y = 0
        self._angle = 0
        self.program = shader.program(
            vertex_shader='''
                #version 330
                uniform mat4 Projection;
                uniform vec2 Position;
                uniform float Angle;

                in vec2 in_vert;
                in vec4 in_color;

                out vec4 v_color;
                void main() {
                    float angle = radians(Angle);
                    mat2 rotate = mat2(
                        cos(angle), sin(angle),
                        -sin(angle), cos(angle)
                    );
                   gl_Position = Projection * vec4(Position + (rotate * in_vert), 0.0, 1.0);
                   v_color = in_color;
                }
            ''',
            fragment_shader='''
                #version 330
                in vec4 v_color;
                out vec4 f_color;
                void main() {
                    f_color = v_color;
                }
            ''',
        )
        # Could do much better using just one vbo and glDrawElementsBaseVertex
        self.batches = defaultdict(_Batch)
        self.dirties = set()

    def append(self, item: TShape):
        """
        Add a new shape to the list.
        """
        self.shape_list.append(item)
        group = (item.mode, item.line_width)
        self.batches[group].items.append(item)
        self.dirties.add(group)

    def remove(self, item: TShape):
        """
        Remove a specific shape from the list.
        """
        self.shape_list.remove(item)
        group = (item.mode, item.line_width)
        self.batches[group].items.remove(item)
        self.dirties.add(group)

    def _refresh_shape(self, group):
        # Create a buffer large enough to hold all the shapes buffers
        batch = self.batches[group]
        total_vbo_bytes = sum(s.vbo.size for s in batch.items)
        vbo = shader.Buffer.create_with_size(total_vbo_bytes)
        offset = 0
        gl.glBindBuffer(gl.GL_COPY_WRITE_BUFFER, vbo.buffer_id)
        # Copy all the shapes buffer in our own vbo
        for shape in batch.items:
            gl.glBindBuffer(gl.GL_COPY_READ_BUFFER, shape.vbo.buffer_id)
            gl.glCopyBufferSubData(
                gl.GL_COPY_READ_BUFFER,
                gl.GL_COPY_WRITE_BUFFER,
                gl.GLintptr(0),
                gl.GLintptr(offset),
                shape.vbo.size)
            offset += shape.vbo.size

        # Create an index buffer object. It should count starting from 0. We need to
        # use a reset_idx to indicate that a new shape will start.
        reset_idx = 2 ** 32 - 1
        indices = []
        counter = itertools.count()
        for shape in batch.items:
            indices.extend(itertools.islice(counter, shape.vao.num_vertices))
            indices.append(reset_idx)
        del indices[-1]
        indices = np.array(indices)
        ibo = shader.Buffer(indices.astype('i4').tobytes())

        vao_content = [
            shader.BufferDescription(
                vbo,
                '2f 4B',
                ('in_vert', 'in_color'),
                normalized=['in_color']
            )
        ]
        vao = shader.vertex_array(self.program, vao_content, ibo)
        with self.program:
            self.program['Projection'] = get_projection().flatten()
            self.program['Position'] = [self.center_x, self.center_y]
            self.program['Angle'] = self.angle

        batch.shape.vao = vao
        batch.shape.vbo = vbo
        batch.shape.ibo = ibo
        batch.shape.program = self.program
        mode, line_width = group
        batch.shape.mode = mode
        batch.shape.line_width = line_width

    def move(self, change_x: float, change_y: float):
        """
        Move all the shapes ion the list
        :param change_x: Amount to move on the x axis
        :param change_y: Amount to move on the y axis
        """
        self.center_x += change_x
        self.center_y += change_y

    def __len__(self) -> int:
        """ Return the length of the sprite list. """
        return len(self.shape_list)

    def __iter__(self) -> Iterable[TShape]:
        """ Return an iterable object of sprites. """
        return iter(self.shape_list)

    def __getitem__(self, i):
        return self.shape_list[i]

    def draw(self):
        """
        Draw everything in the list.
        """
        for group in self.dirties:
            self._refresh_shape(group)
        self.dirties.clear()
        for batch in self.batches.values():
            batch.shape.draw()

    def _get_center_x(self) -> float:
        """Get the center x coordinate of the ShapeElementList."""
        return self._center_x

    def _set_center_x(self, value: float):
        """Set the center x coordinate of the ShapeElementList."""
        self._center_x = value
        with self.program:
            self.program['Position'] = [self._center_x, self._center_y]

    center_x = property(_get_center_x, _set_center_x)

    def _get_center_y(self) -> float:
        """Get the center y coordinate of the ShapeElementList."""
        return self._center_y

    def _set_center_y(self, value: float):
        """Set the center y coordinate of the ShapeElementList."""
        self._center_y = value
        with self.program:
            self.program['Position'] = [self._center_x, self._center_y]

    center_y = property(_get_center_y, _set_center_y)

    def _get_angle(self) -> float:
        """Get the angle of the ShapeElementList in degrees."""
        return self._angle

    def _set_angle(self, value: float):
        """Set the angle of the ShapeElementList in degrees."""
        self._angle = value
        with self.program:
            self.program['Angle'] = self._angle

    angle = property(_get_angle, _set_angle)


class _Batch(Generic[TShape]):
    def __init__(self):
        self.shape = Shape()
        self.items = []


# Internal-Use-Only functions


def _create_line_generic_with_colors(point_list: PointList,
                                    color_list: Iterable[Color],
                                    shape_mode: int,
                                    line_width: float = 1):
    """
    This function is used by ``draw_line_strip`` and ``draw_line_loop``,
    just changing the OpenGL type for the line drawing.

    :param PointList point_list:
    :param Iterable[Color] color_list:
    :param float shape_mode:
    :param float line_width:

    :Returns Shape:
    """
    program = shader.program(
        vertex_shader='''
            #version 330
            uniform mat4 Projection;
            in vec2 in_vert;
            in vec4 in_color;
            out vec4 v_color;
            void main() {
               gl_Position = Projection * vec4(in_vert, 0.0, 1.0);
               v_color = in_color;
            }
        ''',
        fragment_shader='''
            #version 330
            in vec4 v_color;
            out vec4 f_color;
            void main() {
                f_color = v_color;
            }
        ''',
    )

    buffer_type = np.dtype([('vertex', '2f4'), ('color', '4B')])
    data = np.zeros(len(point_list), dtype=buffer_type)
    data['vertex'] = point_list
    data['color'] = [get_four_byte_color(color) for color in color_list]

    vbo = shader.buffer(data.tobytes())
    vao_content = [
        shader.BufferDescription(
            vbo,
            '2f 4B',
            ('in_vert', 'in_color'),
            normalized=['in_color']
        )
    ]

    vao = shader.vertex_array(program, vao_content)
    with vao:
        program['Projection'] = get_projection().flatten()

    shape = Shape()
    shape.vao = vao
    shape.vbo = vbo
    shape.program = program
    shape.mode = shape_mode
    shape.line_width = line_width

    return shape


def _create_line_generic(point_list: PointList,
                        color: Color,
                        shape_mode: int, line_width: float = 1):
    """
    This function is used by ``draw_line_strip`` and ``draw_line_loop``,
    just changing the OpenGL type for the line drawing.
    """
    colors = [get_four_byte_color(color)] * len(point_list)
    shape = _create_line_generic_with_colors(
        point_list,
        colors,
        shape_mode,
        line_width)

    return shape


def _generic_draw_line_strip(point_list: PointList,
                             color: Color,
                             mode: int = gl.GL_LINE_STRIP):
    """
    Draw a line strip. A line strip is a set of continuously connected
    line segments.

    :param point_list: List of points making up the line. Each point is
         in a list. So it is a list of lists.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    """
    # Cache the program. But not on linux because it fails unit tests for some reason.
    # if not _generic_draw_line_strip.program or sys.platform == "linux":

    program = shader.program(
        vertex_shader=_line_vertex_shader,
        fragment_shader=_line_fragment_shader,
    )

    c4 = get_four_byte_color(color)
    c4e = c4 * len(point_list)
    a = array.array('B', c4e)
    color_buf = shader.buffer(a.tobytes())
    color_buf_desc = shader.BufferDescription(
        color_buf,
        '4B',
        ['in_color'],
        normalized=['in_color'],
    )

    def gen_flatten(my_list):
        return [item for sublist in my_list for item in sublist]

    vertices = array.array('f', gen_flatten(point_list))

    vbo_buf = shader.buffer(vertices.tobytes())
    vbo_buf_desc = shader.BufferDescription(
        vbo_buf,
        '2f',
        ['in_vert']
    )

    vao_content = [vbo_buf_desc, color_buf_desc]

    vao = shader.vertex_array(program, vao_content)
    with vao:
        program['Projection'] = get_projection().flatten()
        vao.render(mode=mode)


def _get_points_for_points(point_list, size):
    new_point_list = []
    hs = size / 2
    for point in point_list:
        x = point[0]
        y = point[1]
        new_point_list.append((x - hs, y - hs))
        new_point_list.append((x + hs, y - hs))
        new_point_list.append((x + hs, y + hs))

        new_point_list.append((x + hs, y + hs))
        new_point_list.append((x - hs, y - hs))
        new_point_list.append((x - hs, y + hs))

    return new_point_list


def _create_triangles_filled_with_colors(point_list, color_list):
    shape_mode = gl.GL_TRIANGLE_STRIP
    return _create_line_generic_with_colors(point_list, color_list, shape_mode)


# Utility Functions


def get_rectangle_points(center_x: float, center_y: float, width: float,
                         height: float, tilt_angle: float = 0):
    """
    Utility function that will return all four coordinate points of a
    rectangle given the center_x, center_y, width, height, and rotation.

    Args:
        center_x:
        center_y:
        width:
        height:
        tilt_angle:

    Returns:

    """
    x1 = -width / 2 + center_x
    y1 = -height / 2 + center_y

    x2 = -width / 2 + center_x
    y2 = height / 2 + center_y

    x3 = width / 2 + center_x
    y3 = height / 2 + center_y

    x4 = width / 2 + center_x
    y4 = -height / 2 + center_y

    if tilt_angle:
        x1, y1 = rotate_point(x1, y1, center_x, center_y, tilt_angle)
        x2, y2 = rotate_point(x2, y2, center_x, center_y, tilt_angle)
        x3, y3 = rotate_point(x3, y3, center_x, center_y, tilt_angle)
        x4, y4 = rotate_point(x4, y4, center_x, center_y, tilt_angle)

    data = [(x1, y1),
            (x2, y2),
            (x3, y3),
            (x4, y4)]

    return data


def get_pixel(x: int, y: int) -> Tuple[int, int, int]:
    """
    Given an x, y, will return RGB color value of that point.

    :param int x: x location
    :param int y: y location
    :returns: Color
    """
    # noinspection PyCallingNonCallable,PyTypeChecker

    # The window may be 'scaled' on hi-res displays. Particularly Macs. OpenGL
    # won't account for this, so we need to.
    window = get_window()
    if not window:
        raise ValueError("No window is available to get pixel data from.")

    pixel_ratio = window.get_pixel_ratio()
    x = int(pixel_ratio * x)
    y = int(pixel_ratio * y)

    a = (gl.GLubyte * 3)(0)
    gl.glReadPixels(x, y, 1, 1, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, a)
    red = a[0]
    green = a[1]
    blue = a[2]
    return red, green, blue


def get_image(x: int = 0, y: int = 0, width: int = None, height: int = None):
    """
    Get an image from the screen.

    :param int x: Start (left) x location
    :param int y: Start (top) y location
    :param int width: Width of image. Leave blank for grabbing the 'rest' of the image
    :param int height: Height of image. Leave blank for grabbing the 'rest' of the image

    You can save the image like:

    .. highlight:: python
    .. code-block:: python

        image = get_image()
        image.save('screenshot.png', 'PNG')
    """

    # Get the dimensions
    window = get_window()
    if window is None:
        raise RuntimeError("Handle to the current window is None")
    if width is None:
        width = window.width - x
    if height is None:
        height = window.height - y

    # Create an image buffer
    # noinspection PyTypeChecker
    image_buffer = (gl.GLubyte * (4 * width * height))(0)

    gl.glReadPixels(x, y, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image_buffer)
    image = PIL.Image.frombytes("RGBA", (width, height), image_buffer)
    image = PIL.ImageOps.flip(image)

    # image.save('glutout.png', 'PNG')
    return image


# VBO-Optimized Functions


def draw_line(start_x: float, start_y: float, end_x: float, end_y: float,
                color: Color, line_width: float = 1):
    """
    Draw a simple line, made up of two points.

    :param float start_x:
    :param float start_y:
    :param float end_x:
    :param float end_y:
    :param Color color:
    :param float line_width:

    :Returns Shape:

    """
    id = f"line-{start_x}-{start_y}-{end_x}-{end_y}-{color}-{line_width}"
    if id not in buffered_shapes.keys():
        points = get_points_for_thick_line(start_x, start_y, end_x, end_y, line_width)
        color_list = [color, color, color, color]
        triangle_point_list = points[1], points[0], points[2], points[3]
        shape = _create_triangles_filled_with_colors(triangle_point_list, color_list)
        buffered_shapes[id] = shape
    buffered_shapes[id].draw()


def draw_line_strip(point_list: PointList,
                      color: Color, line_width: float = 1):
    """
    Draw a line made up of multiple points.

    :param PointList point_list:
    :param Color color:
    :param PointList line_width:

    :Returns Shape:

    """
    triangle_point_list: List[Point] = []
    new_color_list: List[Color] = []
    for i in range(1, len(point_list)):
        start_x = point_list[i - 1][0]
        start_y = point_list[i - 1][1]
        end_x = point_list[i][0]
        end_y = point_list[i][1]
        color1 = color
        color2 = color
        id = f"line-{start_x}-{start_y}-{end_x}-{end_y}-{color}-{line_width}"
        if id not in buffered_shapes.keys():
            points = get_points_for_thick_line(start_x, start_y, end_x, end_y, line_width)
            new_color_list += color1, color2, color1, color2
            triangle_point_list += points[1], points[0], points[2], points[3]
            shape = _create_triangles_filled_with_colors(triangle_point_list, new_color_list)
            buffered_shapes[id] = shape
        buffered_shapes[id].draw()


def draw_line_loop(point_list: PointList,
                     color: Color, line_width: float = 1):
    """
    Create a multi-point line loop to be rendered later. This works faster than draw_line because
    the vertexes are only loaded to the graphics card once, rather than each frame.

    :param PointList point_list:
    :param Color color:
    :param float line_width:

    :Returns Shape:

    """
    point_list = list(point_list) + [point_list[0]]
    triangle_point_list: List[Point] = []
    new_color_list: List[Color] = []
    for i in range(1, len(point_list)):
        start_x = point_list[i - 1][0]
        start_y = point_list[i - 1][1]
        end_x = point_list[i][0]
        end_y = point_list[i][1]
        color1 = color
        color2 = color
        id = f"line-{start_x}-{start_y}-{end_x}-{end_y}-{color}-{line_width}"
        if id not in buffered_shapes.keys():
            points = get_points_for_thick_line(start_x, start_y, end_x, end_y, line_width)
            new_color_list += color1, color2, color1, color2
            triangle_point_list += points[1], points[0], points[2], points[3]
            shape = _create_triangles_filled_with_colors(triangle_point_list, new_color_list)
            buffered_shapes[id] = shape
        buffered_shapes[id].draw()


def draw_lines(point_list: PointList,
                 color: Color, line_width: float = 1):
    """
    Draw multiple lines made up of two points.

    :param PointList point_list:
    :param Color color:
    :param float line_width:

    :Returns Shape:

    """
    for i in range(1, len(point_list), 2):
        start_x = point_list[i-1][0]
        start_y = point_list[i-1][1]
        end_x = point_list[i][0]
        end_y = point_list[i][1]
        id = f"line-{start_x}-{start_y}-{end_x}-{end_y}-{color}-{line_width}"
        if id not in buffered_shapes.keys():
            points = get_points_for_thick_line(start_x, start_y, end_x, end_y, line_width)
            color_list = [color, color, color, color]
            triangle_point_list = points[1], points[0], points[2], points[3]
            shape = _create_triangles_filled_with_colors(triangle_point_list, color_list)
            buffered_shapes[id] = shape
        buffered_shapes[id].draw()


def draw_polygon_filled(point_list: PointList,
                   color: Color):
    """
    Draw a convex polygon. This will NOT draw a concave polygon.
    Because of this, you might not want to use this function.

    :param PointList point_list:
    :param color:

    :Returns Shape:

    """
    # We assume points were given in order, either clockwise or counter clockwise.
    # Polygon is assumed to be monotone.
    # To fill the polygon, we start by one vertex, and we chain triangle strips
    # alternating with vertices to the left and vertices to the right of the
    # initial vertex.
    half = len(point_list) // 2
    interleaved = itertools.chain.from_iterable(
        itertools.zip_longest(point_list[:half], reversed(point_list[half:]))
    )
    point_list = [p for p in interleaved if p is not None]
    id = f"polygon-filled-{point_list}-{color}"
    if id not in buffered_shapes.keys():
        shape = _create_line_generic(point_list, color, gl.GL_TRIANGLE_STRIP, 1)
        buffered_shapes[id] = shape
    buffered_shapes[id].draw()


def draw_polygon_outline(point_list: PointList,
                         color: Color, line_width: float = 1):
    """
    Draw a polygon outline. Also known as a "line loop."

    :param PointList point_list: List of points making up the lines. Each point is
         in a list. So it is a list of lists.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param int line_width: Width of the line in pixels.
    """
    point_list = list(point_list) + [point_list[0]]
    triangle_point_list: List[Point] = []
    new_color_list: List[Color] = []
    for i in range(1, len(point_list)):
        start_x = point_list[i - 1][0]
        start_y = point_list[i - 1][1]
        end_x = point_list[i][0]
        end_y = point_list[i][1]
        color1 = color
        color2 = color
        id = f"line-{start_x}-{start_y}-{end_x}-{end_y}-{color}-{line_width}"
        if id not in buffered_shapes.keys():
            points = get_points_for_thick_line(start_x, start_y, end_x, end_y, line_width)
            new_color_list += color1, color2, color1, color2
            triangle_point_list += points[1], points[0], points[2], points[3]
            shape = _create_triangles_filled_with_colors(triangle_point_list, new_color_list)
            buffered_shapes[id] = shape
        buffered_shapes[id].draw()


def draw_rectangle(center_x: float, center_y: float, width: float,
                     height: float, color: Color,
                     border_width: float = 1, tilt_angle: float = 0,
                     filled=True):
    """
    Draw a rectangle.

    Args:
        center_x:
        center_y:
        width:
        height:
        color:
        border_width:
        tilt_angle:
        filled:

    Returns:

    """
    data: List[Point] = cast(List[Point], get_rectangle_points(center_x, center_y, width, height, tilt_angle))

    if filled:
        shape_mode = gl.GL_TRIANGLE_STRIP
        data[-2:] = reversed(data[-2:])
        id = f"rect-filled-{data}-{color}-{border_width}"
    else:
        i_lb = center_x - width / 2 + border_width / 2, center_y - height / 2 + border_width / 2
        i_rb = center_x + width / 2 - border_width / 2, center_y - height / 2 + border_width / 2
        i_rt = center_x + width / 2 - border_width / 2, center_y + height / 2 - border_width / 2
        i_lt = center_x - width / 2 + border_width / 2, center_y + height / 2 - border_width / 2

        o_lb = center_x - width / 2 - border_width / 2, center_y - height / 2 - border_width / 2
        o_rb = center_x + width / 2 + border_width / 2, center_y - height / 2 - border_width / 2
        o_rt = center_x + width / 2 + border_width / 2, center_y + height / 2 + border_width / 2
        o_lt = center_x - width / 2 - border_width / 2, center_y + height / 2 + border_width / 2

        data = [o_lt, i_lt, o_rt, i_rt, o_rb, i_rb, o_lb, i_lb, o_lt, i_lt]

        if tilt_angle != 0:
            point_list_2: List[Point] = []
            for point in data:
                new_point = rotate_point(point[0], point[1], center_x, center_y, tilt_angle)
                point_list_2.append(new_point)
            data = point_list_2

        border_width = 1
        shape_mode = gl.GL_TRIANGLE_STRIP

        # _generic_draw_line_strip(point_list, color, gl.GL_TRIANGLE_STRIP)
        
        # shape_mode = gl.GL_LINE_STRIP
        # data.append(data[0])s

        id = f"rect-empty-{data}-{color}-{border_width}"

    if id not in buffered_shapes.keys():
        shape = _create_line_generic(data, color, shape_mode, border_width)
        buffered_shapes[id] = shape
    buffered_shapes[id].draw()


def draw_rectangle_filled(center_x: float, center_y: float, width: float,
                     height: float, color: Color,
                     border_width: float = 1, tilt_angle: float = 0):
    """
    Draw a rectangle filled.

    :param float center_x:
    :param float center_y:
    :param float width:
    :param float height:
    :param Color color:
    :param float tilt_angle:
    :param float border_width:
    """
    draw_rectangle(center_x, center_y, width, height,
                            color, border_width=border_width, tilt_angle=tilt_angle, filled=True)


def draw_rectangle_outline(center_x: float, center_y: float, width: float,
                     height: float, color: Color,
                     border_width: float = 1, tilt_angle: float = 0):
    """
    Draw a rectangle outline.

    :param float center_x:
    :param float center_y:
    :param float width:
    :param float height:
    :param Color color:
    :param float tilt_angle:
    :param float border_width:
    """
    draw_rectangle(center_x, center_y, width, height,
                            color, border_width=border_width, tilt_angle=tilt_angle, filled=False)


def draw_lrtb_rectangle_filled(left: float, right: float, top: float,
                            bottom: float, color: Color,
                            tilt_angle: float = 0, border_width: float = 1):
    """
    Draw a ltrb rectangle filled.

    :param float left:
    :param float right:
    :param float top:
    :param float bottom:
    :param Color color:
    :param float tilt_angle:
    :param float border_width:
    """
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    width = right - left
    height = top - bottom
    draw_rectangle(center_x, center_y, width, height,
                            color, tilt_angle=tilt_angle, filled=True, border_width=border_width)


def draw_xywh_rectangle_filled(bottom_left_x: float, bottom_left_y: float, width: float,
                            height: float, color: Color, border_width: float = 1,
                            tilt_angle: float = 0):
    """
    Draw a xywh rectangle filled.

    :param float bottom_left_x:
    :param float bottom_left_y:
    :param float width:
    :param float height:
    :param Color color:
    :param float tilt_angle:
    :param float border_width:
    """
    center_x = bottom_left_x + (width / 2)
    center_y = bottom_left_y + (height / 2)
    draw_rectangle(center_x, center_y, width, height,
                            color, border_width=border_width, tilt_angle=tilt_angle, filled=True)


def draw_lrtb_rectangle_outline(left: float, right: float, top: float,
                            bottom: float, color: Color, border_width: float = 1,
                            tilt_angle: float = 0):
    """
    Draw a ltrb rectangle outline.

    :param float left:
    :param float right:
    :param float top:
    :param float bottom:
    :param Color color:
    :param float tilt_angle:
    :param float border_width:
    """
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    width = right - left
    height = top - bottom
    draw_rectangle(center_x, center_y, width, height,
                            color, border_width=border_width, tilt_angle=tilt_angle, filled=False)


def draw_xywh_rectangle_outline(bottom_left_x: float, bottom_left_y: float, width: float,
                            height: float, color: Color, border_width: float = 1,
                            tilt_angle: float = 0):
    """
    Draw a xywh rectangle outline.

    :param float bottom_left_x:
    :param float bottom_left_y:
    :param float width:
    :param float height:
    :param Color color:
    :param float tilt_angle:
    :param float border_width:
    """
    center_x = bottom_left_x + (width / 2)
    center_y = bottom_left_y + (height / 2)
    draw_rectangle(center_x, center_y, width, height,
                            color, border_width=border_width, tilt_angle=tilt_angle, filled=False)


def draw_triangle_outline(x1: float, y1: float,
                          x2: float, y2: float,
                          x3: float, y3: float,
                          color: Color,
                          border_width: float = 1):
    """
    Draw a triangle outline.

    :param float x1: x value of first coordinate.
    :param float y1: y value of first coordinate.
    :param float x2: x value of second coordinate.
    :param float y2: y value of second coordinate.
    :param float x3: x value of third coordinate.
    :param float y3: y value of third coordinate.
    :param Color color: Color of triangle.
    :param float border_width: Width of the border in pixels. Defaults to 1.
    """
    first_point = [x1, y1]
    second_point = [x2, y2]
    third_point = [x3, y3]
    point_list = (first_point, second_point, third_point)
    draw_polygon_outline(point_list, color, border_width)


def draw_ellipse(center_x: float, center_y: float,
                   width: float, height: float, color: Color,
                   border_width: float = 1,
                   tilt_angle: float = 0, num_segments: int = 32,
                   filled=True):

    """
    Draw an ellipse.
    Note: This can't be unit tested on Appveyor because its support for OpenGL is
    poor.
    """
    # Create an array with the vertex point_list
    point_list = []

    for segment in range(num_segments):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = width * math.cos(theta) + center_x
        y = height * math.sin(theta) + center_y

        if tilt_angle:
            x, y = rotate_point(x, y, center_x, center_y, tilt_angle)

        point_list.append((x, y))

    if filled:
        id = f"ellipse-filled-{center_x}-{center_y}-{width}-{height}-{color}-{border_width}-{tilt_angle}-{num_segments}"
        if id not in buffered_shapes.keys():
            half = len(point_list) // 2
            interleaved = itertools.chain.from_iterable(
                itertools.zip_longest(point_list[:half], reversed(point_list[half:]))
            )
            point_list = [p for p in interleaved if p is not None]
            shape_mode = gl.GL_TRIANGLE_STRIP
            shape = _create_line_generic(point_list, color, shape_mode, border_width)
            buffered_shapes[id] = shape
        buffered_shapes[id].draw()
    else:
        id = f"ellipse-empty-{center_x}-{center_y}-{width}-{height}-{color}-{border_width}-{tilt_angle}-{num_segments}"
        if id not in buffered_shapes.keys():
            point_list.append(point_list[0])
            shape_mode = gl.GL_LINE_STRIP
            shape = _create_line_generic(point_list, color, shape_mode, border_width)
            buffered_shapes[id] = shape
        buffered_shapes[id].draw()


def draw_ellipse_filled(center_x: float, center_y: float,
                          width: float, height: float, color: Color,
                          tilt_angle: float = 0, num_segments: int = 128):
    """
    Draw a filled ellipse.
    """

    border_width = 1
    draw_ellipse(center_x, center_y, width, height, color,
                          border_width, tilt_angle, num_segments, filled=True)


def draw_ellipse_outline(center_x: float, center_y: float,
                           width: float, height: float, color: Color,
                           border_width: float = 1,
                           tilt_angle: float = 0, num_segments: int = 128):
    """
    Draw an ellipse outline.
    """

    draw_ellipse(center_x, center_y, width, height, color,
                          border_width, tilt_angle, num_segments, filled=False)


def draw_ellipse_filled_with_colors(center_x: float, center_y: float,
                                      width: float, height: float,
                                      outside_color: Color, inside_color: Color,
                                      tilt_angle: float = 0, num_segments: int = 32):
    """
    Draw an ellipse, and specify inside/outside color. Used for doing gradients.

    :param float center_x:
    :param float center_y:
    :param float width:
    :param float height:
    :param Color outside_color:
    :param float inside_color:
    :param float tilt_angle:
    :param int num_segments:

    :Returns Shape:

    """

    # Create an array with the vertex data
    # Create an array with the vertex point_list
    point_list = [(center_x, center_y)]

    for segment in range(num_segments):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = width * math.cos(theta) + center_x
        y = height * math.sin(theta) + center_y

        if tilt_angle:
            x, y = rotate_point(x, y, center_x, center_y, tilt_angle)

        point_list.append((x, y))
    point_list.append(point_list[1])

    color_list = [inside_color] + [outside_color] * (num_segments + 1)
    id = f"ellipse-filled-with-colors-{point_list}-{color_list}"
    if id not in buffered_shapes.keys():
        shape = _create_line_generic_with_colors(point_list, color_list, gl.GL_TRIANGLE_FAN)
        buffered_shapes[id] = shape
    buffered_shapes[id].draw()


def draw_circle_filled(center_x: float, center_y: float, radius: float,
                       color: Color,
                       num_segments: int = 128):
    """
    Draw a circle filled.

    :param float center_x: x position that is the center of the circle.
    :param float center_y: y position that is the center of the circle.
    :param float radius: width of the circle.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param int num_segments: float of triangle segments that make up this
         circle. Higher is better quality, but slower render time.
    """
    draw_ellipse_filled(center_x, center_y, radius, radius, color, num_segments=num_segments)


def draw_circle_outline(center_x: float, center_y: float, radius: float,
                        color: Color, border_width: float = 1,
                        num_segments: int = 128):
    """
    Draw a circle outline.

    :param float center_x: x position that is the center of the circle.
    :param float center_y: y position that is the center of the circle.
    :param float radius: width of the circle.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param float border_width: Width of the circle outline in pixels.
    :param int num_segments: Int of triangle segments that make up this
         circle. Higher is better quality, but slower render time.
    """
    draw_ellipse_outline(center_x, center_y, radius, radius,
                         color, border_width, num_segments=num_segments)


def draw_point(x: float, y: float, color: Color, size: float):
    """
    Draw a point.

    :param float x: x position of point.
    :param float y: y position of point.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param float size: Size of the point in pixels.
    """
    draw_rectangle_filled(x, y, size / 2, size / 2, color)


# VBO-Unoptimized Functions


def draw_triangle_filled(x1: float, y1: float,
                         x2: float, y2: float,
                         x3: float, y3: float, color: Color):
    """
    Draw a triangle filled.

    :param float x1: x value of first coordinate.
    :param float y1: y value of first coordinate.
    :param float x2: x value of second coordinate.
    :param float y2: y value of second coordinate.
    :param float x3: x value of third coordinate.
    :param float y3: y value of third coordinate.
    :param Color color: Color of triangle.
    """

    first_point = (x1, y1)
    second_point = (x2, y2)
    third_point = (x3, y3)
    point_list = (first_point, second_point, third_point)
    _generic_draw_line_strip(point_list, color, gl.GL_TRIANGLES)


def draw_arc_filled(center_x: float, center_y: float,
                    width: float, height: float,
                    color: Color,
                    start_angle: float, end_angle: float,
                    tilt_angle: float = 0,
                    num_segments: int = 128):
    """
    Draw a filled in arc. Useful for drawing pie-wedges, or Pac-Man.

    :param float center_x: x position that is the center of the arc.
    :param float center_y: y position that is the center of the arc.
    :param float width: width of the arc.
    :param float height: height of the arc.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param float start_angle: start angle of the arc in degrees.
    :param float end_angle: end angle of the arc in degrees.
    :param float tilt_angle: angle the arc is tilted.
    :param float num_segments: Number of line segments used to draw arc.
    """
    unrotated_point_list = [[0.0, 0.0]]

    start_segment = int(start_angle / 360 * num_segments)
    end_segment = int(end_angle / 360 * num_segments)

    for segment in range(start_segment, end_segment + 1):
        theta = 2.0 * 3.1415926 * segment / num_segments

        x = width * math.cos(theta) / 2
        y = height * math.sin(theta) / 2

        unrotated_point_list.append([x, y])

    if tilt_angle == 0:
        uncentered_point_list = unrotated_point_list
    else:
        uncentered_point_list = []
        for point in unrotated_point_list:
            uncentered_point_list.append(rotate_point(point[0], point[1], 0, 0, tilt_angle))

    point_list = []
    for point in uncentered_point_list:
        point_list.append((point[0] + center_x, point[1] + center_y))

    _generic_draw_line_strip(point_list, color, gl.GL_TRIANGLE_FAN)


def draw_arc_outline(center_x: float, center_y: float, width: float,
                     height: float, color: Color,
                     start_angle: float, end_angle: float,
                     border_width: float = 1, tilt_angle: float = 0,
                     num_segments: int = 128):
    """
    Draw the outside edge of an arc. Useful for drawing curved lines.

    :param float center_x: x position that is the center of the arc.
    :param float center_y: y position that is the center of the arc.
    :param float width: width of the arc.
    :param float height: height of the arc.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param float start_angle: start angle of the arc in degrees.
    :param float end_angle: end angle of the arc in degrees.
    :param float border_width: width of line in pixels.
    :param float tilt_angle: angle the arc is tilted.
    :param int num_segments: float of triangle segments that make up this
         circle. Higher is better quality, but slower render time.
    """
    unrotated_point_list = []

    start_segment = int(start_angle / 360 * num_segments)
    end_segment = int(end_angle / 360 * num_segments)

    inside_width = (width - border_width / 2) / 2
    outside_width = (width + border_width / 2) / 2
    inside_height = (height - border_width / 2) / 2
    outside_height = (height + border_width / 2) / 2

    for segment in range(start_segment, end_segment + 1):
        theta = 2.0 * math.pi * segment / num_segments

        x1 = inside_width * math.cos(theta)
        y1 = inside_height * math.sin(theta)

        x2 = outside_width * math.cos(theta)
        y2 = outside_height * math.sin(theta)

        unrotated_point_list.append([x1, y1])
        unrotated_point_list.append([x2, y2])

    if tilt_angle == 0:
        uncentered_point_list = unrotated_point_list
    else:
        uncentered_point_list = []
        for point in unrotated_point_list:
            uncentered_point_list.append(rotate_point(point[0], point[1], 0, 0, tilt_angle))

    point_list = []
    for point in uncentered_point_list:
        point_list.append((point[0] + center_x, point[1] + center_y))

    _generic_draw_line_strip(point_list, color, gl.GL_TRIANGLE_STRIP)


def draw_parabola_filled(start_x: float, start_y: float, end_x: float,
                         height: float, color: Color,
                         tilt_angle: float = 0):
    """
    Draws a filled in parabola.

    :param float start_x: The starting x position of the parabola
    :param float start_y: The starting y position of the parabola
    :param float end_x: The ending x position of the parabola
    :param float height: The height of the parabola
    :param Color color: The color of the parabola
    :param float tilt_angle: The angle of the tilt of the parabola

    """
    center_x = (start_x + end_x) / 2
    center_y = start_y + height
    start_angle = 0
    end_angle = 180
    width = (start_x - end_x)
    draw_arc_filled(center_x, center_y, width, height, color,
                    start_angle, end_angle, tilt_angle)


def draw_parabola_outline(start_x: float, start_y: float, end_x: float,
                          height: float, color: Color,
                          border_width: float = 1, tilt_angle: float = 0):
    """
    Draws the outline of a parabola.

    :param float start_x: The starting x position of the parabola
    :param float start_y: The starting y position of the parabola
    :param float end_x: The ending x position of the parabola
    :param float height: The height of the parabola
    :param Color color: The color of the parabola
    :param float border_width: The width of the parabola
    :param float tilt_angle: The angle of the tilt of the parabola
    """
    center_x = (start_x + end_x) / 2
    center_y = start_y + height
    start_angle = 0
    end_angle = 180
    width = (start_x - end_x)
    draw_arc_outline(center_x, center_y, width, height, color,
                     start_angle, end_angle, border_width, tilt_angle)


def draw_points(point_list: PointList,
                color: Color, size: float = 1):
    """
    Draw a set of points.

    :param PointList point_list: List of points Each point is
         in a list. So it is a list of lists.
    :param Color color: color, specified in a list of 3 or 4 bytes in RGB or
         RGBA format.
    :param float size: Size of the point in pixels.
    """
    new_point_list = _get_points_for_points(point_list, size)
    _generic_draw_line_strip(new_point_list, color, gl.GL_TRIANGLES)


def draw_scaled_texture_rectangle(center_x: float, center_y: float,
                                  texture: Texture,
                                  scale: float = 1.0,
                                  angle: float = 0,
                                  alpha: int = 255):
    """
    Draw a textured rectangle.

    :param float center_x: x coordinate of rectangle center.
    :param float center_y: y coordinate of rectangle center.
    :param int texture: identifier of texture returned from load_texture() call
    :param float scale: scale of texture
    :param float angle: rotation of the rectangle. Defaults to zero.
    :param float alpha: Transparency of image. 0 is fully transparent, 255 (default) is visible
    """

    texture.draw_scaled(center_x, center_y, scale, angle, alpha)


def draw_texture_rectangle(center_x: float, center_y: float,
                           width: float,
                           height: float,
                           texture: Texture,
                           angle: float = 0,
                           alpha: int = 255):
    """
    Draw a textured rectangle on-screen.

    :param float center_x: x coordinate of rectangle center.
    :param float center_y: y coordinate of rectangle center.
    :param float width: width of texture
    :param float height: height of texture
    :param int texture: identifier of texture returned from load_texture() call
    :param float angle: rotation of the rectangle. Defaults to zero.
    :param float alpha: Transparency of image. 0 is fully transparent, 255 (default) is visible
    """

    texture.draw_sized(center_x, center_y, width, height, angle, alpha)


def draw_lrwh_rectangle_textured(bottom_left_x: float, bottom_left_y: float,
                                 width: float,
                                 height: float,
                                 texture: Texture, angle: float = 0,
                                 alpha: int = 255):
    """
    Draw a texture extending from bottom left to top right.

    :param float bottom_left_x: The x coordinate of the left edge of the rectangle.
    :param float bottom_left_y: The y coordinate of the bottom of the rectangle.
    :param float width: The width of the rectangle.
    :param float height: The height of the rectangle.
    :param int texture: identifier of texture returned from load_texture() call
    :param float angle: rotation of the rectangle. Defaults to zero.
    :param int alpha: Transparency of image. 0 is fully transparent, 255 (default) is visible
    """

    center_x = bottom_left_x + (width / 2)
    center_y = bottom_left_y + (height / 2)
    texture.draw_sized(center_x, center_y, width, height, angle=angle, alpha=alpha)
