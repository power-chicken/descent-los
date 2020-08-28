import pygame
# from pygame.locals import *
from math import floor
import numpy as np

rgb_red = (255, 0, 0)
rgb_black = (0, 0, 0)
rgb_blue = (0, 0, 255)
rgb_white = (255, 255, 255)
rgb_green = (0, 255, 0)
rgb_gray = (100, 100, 100)
rgb_yellow = (255, 255, 0)


class Tile:

    def __init__(self, x, y, pygame_display_surf):

        self.x = x
        self.y = y

        self.n_lines_see_this_tile = 0
        self.type = 'empty'

        self.pygame_display_surf = pygame_display_surf

        self.width = 40
        self.height = 40

        self.grid_line_width = 3

    def get_left_pixel_value(self):

        return self.x * self.width

    def get_top_pixel_value(self):

        return self.y * self.height

    def get_outer_color(self):

        if self.type == 'empty':
            return rgb_gray
        elif self.type == 'hero':
            return rgb_blue
        elif self.type == 'monster':
            return rgb_red
        elif self.type == 'obstacle':
            return rgb_black
        else:
            return rgb_white

    def get_inner_color(self):
        if self.n_lines_see_this_tile > 0:
            return rgb_yellow
        else:
            return rgb_red

    def draw(self):

        pygame.draw.rect(self.pygame_display_surf, rgb_black,
                         (self.get_left_pixel_value(), self.get_top_pixel_value(), self.width, self.height),
                         self.grid_line_width)

        pygame.draw.rect(self.pygame_display_surf, self.get_outer_color(),
                         (self.get_left_pixel_value() + 2, self.get_top_pixel_value() + 2, self.width - 4,
                          self.height - 4), 0)

        pygame.draw.rect(self.pygame_display_surf, self.get_inner_color(),
                         (self.get_left_pixel_value() + 15, self.get_top_pixel_value() + 15, self.width - 30,
                          self.height - 30), 0)

        system_font = pygame.font.SysFont("comicsansms", size=16)
        text_hero_surface = system_font.render("{}".format(self.n_lines_see_this_tile), True, rgb_white)
        self.pygame_display_surf.blit(text_hero_surface,
                                      (self.get_left_pixel_value() + 5, self.get_top_pixel_value() + 7))

    def get_top_left_corner(self):

        return np.array([self.x, self.y])

    def get_top_right_corner(self):

        return np.array([self.x + 1, self.y])

    def get_bottom_left_corner(self):

        return np.array([self.x, self.y + 1])

    def get_bottom_right_corner(self):

        return np.array([self.x + 1, self.y + 1])

    def get_all_corners(self):

        return [self.get_top_left_corner(), self.get_top_right_corner(),
                self.get_bottom_left_corner(), self.get_bottom_right_corner()]

    def get_center(self):

        return np.array([self.get_left_pixel_value() + self.width / 2, self.get_top_pixel_value() + self.height / 2])


class Grid:

    def __init__(self, pygame_display_surf):

        self._n_tiles_x, self._n_tiles_y = 8, 8

        # draw parameter
        self._square_size = 40
        self._grid_line_width = 3
        self._distance_from_window = 0

        self._tiles = [[Tile(x, y, pygame_display_surf) for y in range(self._n_tiles_y)]
                       for x in range(self._n_tiles_x)]

        self._hero_tile = None

        self.use_rule_center_to_center = False
        self.use_rule_corner_to_corner = True

    def get_all_tiles_as_1d_list(self):

        tile_list = []
        for tile_line in self._tiles:
            for tile in tile_line:
                tile_list.append(tile)

        return tile_list

    def _init_default_los(self):

        for tile in self.get_all_tiles_as_1d_list():
            tile.n_lines_see_this_tile = 0

    def _get_hero_location_is_valid(self):

        return self._hero_tile is not None

    def draw_all_tiles(self):

        for tile in self.get_all_tiles_as_1d_list():
            tile.draw()

    def get_tile_coordinates_from_pixel(self, cursor_pos):

        x_coord = (cursor_pos[0] - self._distance_from_window) / self._square_size
        y_coord = (cursor_pos[1] - self._distance_from_window) / self._square_size

        return x_coord, y_coord

    def get_tile_from_tile_coordinates(self, x_coord, y_coord):

        if self.is_tile_location_valid(floor(x_coord), floor(y_coord)):
            return self._tiles[floor(x_coord)][floor(y_coord)]
        else:
            return None

    def get_tile_from_pixel(self, cursor_pos):

        x_coord, y_coord = self.get_tile_coordinates_from_pixel(cursor_pos)

        return self.get_tile_from_tile_coordinates(x_coord, y_coord)

    def is_tile_location_valid(self, x, y):

        return 0 <= x < self._n_tiles_x and 0 <= y < self._n_tiles_y

    def set_tile_type(self, tile, new_tile_type):

        # only do something when requesting a valid tile
        if tile is None:
            return

        # if requesting the same type on the as it is, change it to empty. Otherwise change as requested
        if tile.type == new_tile_type:
            tile.type = 'empty'

            # if removed the hero, erase the reference
            if new_tile_type == 'hero':
                self._hero_tile = None

        else:
            if tile is self._hero_tile:
                self._hero_tile = None

            tile.type = new_tile_type

            # if a new hero location is set, make the old empty and set new reference
            if new_tile_type == 'hero':
                if self._get_hero_location_is_valid():
                    self._hero_tile.type = 'empty'
                self._hero_tile = tile

        self.recompute_los()

    def get_all_tiles_in_line_by_sampling_pixels(self, start_location, end_location):

        intersecting_tiles = []

        location_diff = end_location - start_location

        n_samples_on_line = floor(10 * (abs(location_diff[0]) + abs(location_diff[1])) / self._square_size)

        for i in range(n_samples_on_line):

            location_sample = start_location + i / (n_samples_on_line - 1) * location_diff

            tile = self.get_tile_from_pixel(location_sample)

            if tile not in intersecting_tiles and tile is not None:
                intersecting_tiles.append(tile)

        return intersecting_tiles

    def get_all_tiles_in_line_discrete(self, start_corner, end_corner):

        intersecting_tiles = []

        corner_diff = end_corner - start_corner

        if corner_diff[0] == 0:
            return self.get_all_tiles_along_vertical_line(start_corner, corner_diff[1])
        elif corner_diff[1] == 0:
            return self.get_all_tiles_along_horizontal_line(start_corner, corner_diff[0])
        if abs(corner_diff[0]) == abs(corner_diff[1]):
            if corner_diff[0] == 0:
                return None
            return self.get_all_tiles_along_diagonal_line(start_corner, corner_diff)
        else:
            return None

    def get_all_tiles_along_vertical_line(self, start_corner, n_tiles_in_y_direction):

        tiles_along_vertical_line = []

        trace_downwards = n_tiles_in_y_direction > 0

        incrementer = 1 if trace_downwards else -1

        for i in range(0, n_tiles_in_y_direction, incrementer):
            for x_add in [-1, 0]:  # this results in checks left and right from the line

                x = start_corner[0] + x_add
                y = start_corner[1] + i
                if not trace_downwards:
                    y += -1

                if self.is_tile_location_valid(x, y):
                    tiles_along_vertical_line.append(self._tiles[x][y])

        return tiles_along_vertical_line

    def get_all_tiles_along_horizontal_line(self, start_corner, n_tiles_in_x_direction):

        tiles_along_horizontal_line = []

        trace_right = n_tiles_in_x_direction > 0

        incrementer = 1 if trace_right else -1

        for i in range(0, n_tiles_in_x_direction, incrementer):
            for y_add in [-1, 0]:  # this results in checks up and down from the line

                x = start_corner[0] + i
                y = start_corner[1] + y_add
                if not trace_right:
                    x += -1

                if self.is_tile_location_valid(x, y):
                    tiles_along_horizontal_line.append(self._tiles[x][y])

        return tiles_along_horizontal_line

    def get_all_tiles_along_diagonal_line(self, start_corner, difference_vector):

        tiles_along_line = []

        if abs(difference_vector[0]) != abs(difference_vector[1]):
            raise RuntimeError("invalid use of this function.")

        n_tiles_crossed_by_the_line = abs(difference_vector[0])
        direction = difference_vector // n_tiles_crossed_by_the_line

        x_sum = -1 if direction[0] == -1 else 0
        y_sum = -1 if direction[1] == -1 else 0

        for i in range(n_tiles_crossed_by_the_line):
            x = start_corner[0] + i * direction[0] + x_sum
            y = start_corner[1] + i * direction[1] + y_sum

            tiles_along_line.append(self._tiles[x][y])

        return tiles_along_line

    def get_all_tiles_along_non_grid_parallel_line(self, start_corner, difference_vector):

        tiles_along_line = []

        return tiles_along_line

    def recompute_los(self):

        self._init_default_los()

        if not self._get_hero_location_is_valid():
            return

        for target_tile in self.get_all_tiles_as_1d_list():
            if target_tile is self._hero_tile:
                continue

            if self.use_rule_center_to_center:
                tiles_in_line_from_hero = self.get_all_tiles_in_line_by_sampling_pixels(
                    self._hero_tile.get_center(),
                    target_tile.get_center())

                if not any(tile.type == 'obstacle' or tile.type == 'monster' for tile in tiles_in_line_from_hero):
                    target_tile.n_lines_see_this_tile += 1

            if self.use_rule_corner_to_corner:
                for hero_tile_corner in self._hero_tile.get_all_corners():
                    for target_tile_corner in target_tile.get_all_corners():

                        tiles_in_line_from_hero = self.get_all_tiles_in_line_discrete(hero_tile_corner,
                                                                                      target_tile_corner)

                        if tiles_in_line_from_hero is None:
                            continue
                        if not any(tile.type == 'obstacle'
                                   or tile.type == 'monster'
                                   or tile.type == 'hero'
                                   for tile in tiles_in_line_from_hero):
                            target_tile.n_lines_see_this_tile += 1
