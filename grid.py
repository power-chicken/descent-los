import pygame
# from pygame.locals import *
from math import floor

rgb_red = (255, 0, 0)
rgb_black = (0, 0, 0)
rgb_blue = (0, 0, 255)
rgb_white = (255, 255, 255)
rgb_green = (0, 255, 0)
rgb_gray = (100, 100, 100)
rgb_yellow = (0, 255, 255)


class Tile:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.los = False
        self.type = 'empty'

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


class Grid:

    def __init__(self):
        self._n_tiles_x, self._n_tiles_y = 12, 10

        # draw parameter
        self._square_size = 40
        self._grid_line_width = 3
        self._distance_from_window = 5

        self._tiles = [Tile(x, y) for x in range(self._n_tiles_x) for y in range(self._n_tiles_y)]

        self._hero_tile = None

    def _init_default_los(self):

        for tile in self._tiles:
            tile.los = False

    def _get_hero_location_is_valid(self):

        return self._hero_tile is not None

    def draw_grid_lines(self, pygame_display_surf):

        for tile in self._tiles:
            pygame.draw.rect(pygame_display_surf, rgb_black,
                             (self._distance_from_window + tile.x * self._square_size,
                              self._distance_from_window + tile.y * self._square_size,
                              self._square_size,
                              self._square_size), self._grid_line_width)

    def draw_cells(self, pygame_display_surf):

        for tile in self._tiles:

            pygame.draw.rect(pygame_display_surf, tile.get_outer_color(),
                             (self._distance_from_window + tile.x * self._square_size + 2,
                              self._distance_from_window + tile.y * self._square_size + 2,
                              self._square_size - 4,
                              self._square_size - 4), 0)

            if tile.los:
                pygame.draw.rect(pygame_display_surf, tile.get_inner_color(),
                                 (self._distance_from_window + tile.x * self._square_size + 8,
                                  self._distance_from_window + tile.y * self._square_size + 8,
                                  self._square_size - 16,
                                  self._square_size - 16), 0)

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

        #self.recompute_los()

    def get_all_tiles_in_line(self, start_location, end_location):

        intersecting_tiles = []

        location_diff = end_location - start_location

        n_samples_on_line = location_diff[0] + location_diff[1]

        for i in range(n_samples_on_line):

            location_sample = start_location + i / (n_samples_on_line - 1) * location_diff

            tile_row, tile_column = self.get_tile_from_tile_coordinates(location_sample[1], location_sample[0])

            if (tile_row, tile_column) not in intersecting_tiles:
                intersecting_tiles.append((tile_row, tile_column))

        return intersecting_tiles

    def recompute_los(self):

        if not self._get_hero_location_is_valid():
            self._init_default_los()
            return

        else:

            tiles_in_line_from_hero = self.get_all_tiles_in_line(self._hero_location, (0, 0))

            for tile in tiles_in_line_from_hero:

                self._cell_los[tile[0]][tile[1]] = 'los'
