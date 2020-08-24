import pygame
from pygame.locals import *
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

        self._cells = [['empty' for i in range(self._n_rows)] for j in range(self._n_columns)]

    def draw(self, pygame_display_surf):

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

                cell_type = self._cells[i_col][i_row]

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

    def set_tile_type(self, tile_row, tile_column, tile_type):

        if tile_row < 0 or tile_row >= self._n_rows or tile_column < 0 or tile_column >= self._n_columns:
            return

        if self._cells[tile_column][tile_row] == tile_type:
            self._cells[tile_column][tile_row] = 'empty'
        else:
            self._cells[tile_column][tile_row] = tile_type
