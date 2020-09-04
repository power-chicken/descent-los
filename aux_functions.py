from math import floor, ceil, isclose
from global_constants import *


def is_value_almost_integer(value):

    return isclose(value, floor(value)) or isclose(value, ceil(value))


def get_color_by_tile_type(tile_type):

    if tile_type == 'empty':
        return rgb_white
    elif tile_type == 'hero':
        return rgb_blue
    elif tile_type == 'monster':
        return rgb_red
    elif tile_type == 'obstacle':
        return rgb_gray
    else:
        return rgb_gray
