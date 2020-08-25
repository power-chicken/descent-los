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
rgb_yellow = (0, 255, 255)


class Tile:

    def __init__(self, x, y, pygame_display_surf):

        self.x = x
        self.y = y

        self.los = False
        self.type = 'empty'

        self.pygame_display_surf = pygame_display_surf

        self.width = 40
        self.height = 40

        self.pos_left = x * self.width
        self.pos_top = y * self.height

        self.grid_line_width = 3

    def get_outer_color(self):

        if self.type == 'empty':
            return rgb_gray
        elif self.type == 'hero':
            return rgb_blue
        elif self.type == 'monster':
            return rgb_red
        elif self.type == 'obstacle':
            return rgb_green
        else:
            return rgb_white

    def get_inner_color(self):
        if self.los:
            return rgb_yellow
        else:
            return rgb_red

    def draw(self):

        pygame.draw.rect(self.pygame_display_surf, rgb_black,
                         (self.pos_left, self.pos_top, self.width, self.height), self.grid_line_width)

        pygame.draw.rect(self.pygame_display_surf, self.get_outer_color(),
                         (self.pos_left + 2, self.pos_top + 2, self.width - 4, self.height - 4), 0)

        if self.los:
            pygame.draw.rect(self.pygame_display_surf, self.get_inner_color(),
                             (self.pos_left + 8, self.pos_top + 8, self.width - 16, self.height - 16), 0)

    def get_top_left_corner(self):

        return np.array([self.pos_left, self.pos_top])

    def get_top_right_corner(self):

        return np.array([self.pos_left + self.width, self.pos_top])

    def get_bottom_left_corner(self):

        return np.array([self.pos_left, self.pos_top + self.height])

    def get_bottom_right_corner(self):

        return np.array([self.pos_left + self.width, self.pos_top + self.height])

    def get_all_corners(self):

        return [self.get_top_left_corner(), self.get_top_right_corner(),
                self.get_bottom_left_corner(), self.get_bottom_right_corner()]

    def get_center(self):

        return np.array([self.pos_left + self.width / 2, self.pos_top + self.height / 2])


class Grid:

    def __init__(self, pygame_display_surf):

        self._n_tiles_x, self._n_tiles_y = 12, 10

        # draw parameter
        self._square_size = 40
        self._grid_line_width = 3
        self._distance_from_window = 0

        self._tiles = [Tile(x, y, pygame_display_surf) for x in range(self._n_tiles_x) for y in range(self._n_tiles_y)]

        self._hero_tile = None

    def _init_default_los(self):

        for tile in self._tiles:
            tile.los = False

    def _get_hero_location_is_valid(self):

        return self._hero_tile is not None

    def draw_all_tiles(self):

        for tile in self._tiles:
            tile.draw()

    def get_tile_coordinates_from_pixel(self, cursor_pos):

        x_coord = (cursor_pos[0] - self._distance_from_window) / self._square_size
        y_coord = (cursor_pos[1] - self._distance_from_window) / self._square_size

        return x_coord, y_coord

    def get_tile_from_tile_coordinates(self, x_coord, y_coord):

        for tile in self._tiles:
            if floor(x_coord) == tile.x and floor(y_coord) == tile.y:
                return tile

        return None

    def get_tile_from_pixel(self, cursor_pos):

        x_coord, y_coord = self.get_tile_coordinates_from_pixel(cursor_pos)

        return self.get_tile_from_tile_coordinates(x_coord, y_coord)

    def is_tile_location_valid(self, x, y):

        return 0 <= x < self._n_tiles_x and 0 <= y < self._n_tiles_y

    def set_tile_type(self, tile, new_tile_type):

        # only do something when requesting a valid location
        if tile is None:
            return

        # if requesting the same type on the as it is, change it to empty. Otherwise change as requested
        if tile.type == new_tile_type:
            tile.type = 'empty'

            # if removed the hero, erase the reference
            if new_tile_type == 'hero':
                self._hero_tile = None

        else:
            tile.type = new_tile_type

            # if a new hero location is set, make the old empty and set new reference
            if new_tile_type == 'hero':
                if self._get_hero_location_is_valid():
                    self._hero_tile.type = 'empty'
                self._hero_tile = tile

        self.recompute_los()

    def get_all_tiles_in_line(self, start_location, end_location):

        intersecting_tiles = []

        location_diff = end_location - start_location

        n_samples_on_line = floor(10 * (abs(location_diff[0]) + abs(location_diff[1])) / self._square_size)

        for i in range(n_samples_on_line):

            location_sample = start_location + i / (n_samples_on_line - 1) * location_diff

            tile = self.get_tile_from_pixel(location_sample)

            if tile not in intersecting_tiles and tile is not None:
                intersecting_tiles.append(tile)

        return intersecting_tiles

    def recompute_los(self):

        self._init_default_los()

        if self._get_hero_location_is_valid():

            for target_tile in self._tiles:

                # center -> center rule
                tiles_in_line_from_hero = self.get_all_tiles_in_line(self._hero_tile.get_center(),
                                                                     target_tile.get_center())

                target_tile.los = not any(tile.type == 'obstacle'
                                          or tile.type == 'monster' for tile in tiles_in_line_from_hero)

                if not target_tile.los:
                    # corner -> corner rule
                    for hero_tile_corner in self._hero_tile.get_all_corners():
                        for target_tile_corner in target_tile.get_all_corners():
                            tiles_in_line_from_hero = self.get_all_tiles_in_line(hero_tile_corner,
                                                                                 target_tile_corner)

                            target_tile.los = not any(tile.type == 'obstacle'
                                                      or tile.type == 'monster' for tile in tiles_in_line_from_hero)
