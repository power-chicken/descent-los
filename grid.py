import pygame
# from pygame.locals import *
from math import floor

rgb_red = (255, 0, 0)
rgb_black = (0, 0, 0)
rgb_blue = (0, 0, 255)
rgb_white = (255, 255, 255)
rgb_green = (0, 255, 0)
rgb_gray = (100, 100, 100)


class Grid:

    def __init__(self):
        self._n_rows, self._n_columns = 10, 12
        self._square_size = 40
        self._grid_line_width = 3

        self._distance_from_window = 5

        self._cells = [['empty' for _ in range(self._n_columns)] for _ in range(self._n_rows)]

        self._hero_location = (-1, -1)  # there can be only one hero

    def draw_grid_lines(self, pygame_display_surf):

        for i_row in range(self._n_rows):
            for i_col in range(self._n_columns):
                pygame.draw.rect(pygame_display_surf, rgb_black,
                                 (self._distance_from_window + i_col * self._square_size,
                                  self._distance_from_window + i_row * self._square_size,
                                  self._square_size,
                                  self._square_size), self._grid_line_width)

    def draw_cells(self, pygame_display_surf):
        for i_row in range(self._n_rows):
            for i_col in range(self._n_columns):

                cell_type = self._cells[i_row][i_col]

                if cell_type == 'empty':
                    cell_color = rgb_gray
                elif cell_type == 'hero':
                    cell_color = rgb_blue
                elif cell_type == 'monster':
                    cell_color = rgb_red
                elif cell_type == 'obstacle':
                    cell_color = rgb_green
                else:
                    cell_color = rgb_white

                pygame.draw.rect(pygame_display_surf, cell_color,
                                 (self._distance_from_window + i_col * self._square_size + 2,
                                  self._distance_from_window + i_row * self._square_size + 2,
                                  self._square_size - 4,
                                  self._square_size - 4), 0)

    def get_tile_from_pixel(self, cursor_pos):

        tile_row = floor((cursor_pos[1] - self._distance_from_window) / self._square_size)
        tile_column = floor((cursor_pos[0] - self._distance_from_window) / self._square_size)

        return tile_row, tile_column

    def is_tile_location_valid(self, tile_row, tile_column):

        return 0 <= tile_row < self._n_rows and 0 <= tile_column < self._n_columns

    def set_tile_type(self, tile_row, tile_column, tile_type):

        if not self.is_tile_location_valid(tile_row, tile_column):
            return

        if self._cells[tile_row][tile_column] == tile_type:
            self._cells[tile_row][tile_column] = 'empty'
        else:
            self._cells[tile_row][tile_column] = tile_type

        if tile_type == 'hero':
            if self.is_tile_location_valid(self._hero_location[0], self._hero_location[1]):
                self._cells[self._hero_location[0]][self._hero_location[1]] = 'empty'
            self._hero_location = (tile_row, tile_column)
