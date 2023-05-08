
from svg.path.path import Line, CubicBezier
from xml.dom import minidom
from kivy.utils import get_color_from_hex
import os


def do_correction_path(path_filename):
		bar_init = '/' if path_filename.startswith('/') else ''
		new_str = []

		for x in path_filename.split('\\'):
			new_str.extend(x.split(r'/'))

		path = [f'{x}/' for x in new_str[0:-1] if x != '']
		return ''.join([bar_init] + path + [new_str[-1]])

root_path = do_correction_path(os.path.split(__file__)[0])


def rgb_2_dec(color):
	return [channel / 255 for channel in color]


def dec_2_rgb(color):
	return [int(channel * 255) for channel in color]



# working with ratio to get a given svg path coordinate wrt to given widget
"""
x_pos, y_pos: svg path coordinate
wx, wy: widget pos
w, h: widget size
sw, sh: svg size
sf: svg_file, only needed for kivy icon support
"""
# Special support for Kivy svg Icon :)

def x(x_pos, wx, w, sw, sf):

    if "kivy" in sf:
        return ( wx + ( w * (x_pos / 10) / sw) )
    
    return ( wx + (w * x_pos / sw) )


def y(y_pos, wy, h, sh, sf):
    
    if "kivy" in sf:
        return ( wy + (h * ((y_pos / 10)) / sh) )
    
    return ( wy + (h * (sh - y_pos) / sh) )


def point(complex_point: complex, w, h, wx, wy, sw, sh, sf): 
    return [
        x(complex_point.real, wx, w, sw, sf),
        y(complex_point.imag, wy, h, sh, sf)
    ]


def bezier_points(e: CubicBezier, w, h, wx, wy, sw, sh, sf):
    return [
        *point(e.start, w, h, wx, wy, sw, sh, sf),
        *point(e.control1, w, h, wx, wy, sw, sh, sf),
        *point(e.control2, w, h, wx, wy, sw, sh, sf),
        *point(e.end, w, h, wx, wy, sw, sh, sf),
    ]


def line_points(e: Line, w, h, wx, wy, sw, sh, sf):
    return [
        *point(e.start, w, h, wx, wy, sw, sh, sf),
        *point(e.end, w, h, wx, wy, sw, sh, sf),
    ]


# https://stackoverflow.com/a/15399173/8871954
def B0_t(t):
    return (1 - t) ** 3

def B1_t(t):
    return 3 * t * (1 - t) ** 2

def B2_t(t):
    return 3 * t ** 2 * (1 - t)

def B3_t(t):
    return t ** 3


def get_all_points(start, c1, c2, end):
    points = []
    ax, ay = start
    dx, dy = end
    bx, by = c1
    cx, cy = c2

    seg = 1 / 40
    t = 0

    while t <= 1:
        points.extend(
            [
                (B0_t(t) * ax) + (B1_t(t) * bx) + (B2_t(t) * cx) + (B3_t(t) * dx),
                (B0_t(t) * ay) + (B1_t(t) * by) + (B2_t(t) * cy) + (B3_t(t) * dy),
            ]
        )
        t += seg

    return points

def parse_svg(svg_file):
    doc = minidom.parse(svg_file)

    viewbox_string = doc.getElementsByTagName("svg")[0].getAttribute("viewBox")

    sep = "," if "," in viewbox_string else " "
    sw_size = list( map(int, viewbox_string.split(sep)[2:]) )
    
    path_count = 0
    path_strings = []

    for path in doc.getElementsByTagName("path"):
        id_ = path.getAttribute("id") or f"path_{path_count}"
        d = path.getAttribute("d")
        try:
            clr = get_color_from_hex(path.getAttribute("fill")) or [1, 1, 1, 0]
        except ValueError:
            # if color format is different
            clr = [1, 1, 1, 0]

        path_strings.append((d, id_, clr))
        path_count += 1
    
    doc.unlink()
    return [sw_size, path_strings]

def find_center(input_list):
    middle = float(len(input_list)) / 2
    
    if middle % 2 != 0:
        return input_list[int(middle - 0.5)]
    
    return ( (input_list[int(middle)] + input_list[int(middle-1)]) / 2 )


