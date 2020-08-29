from math import floor, ceil, isclose


def is_value_almost_integer(value):

    return isclose(value, floor(value)) or isclose(value, ceil(value))
