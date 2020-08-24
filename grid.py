import pygame
from pygame.locals import *


class Grid:

    def __init__(self):
        self._n_rows, self._n_columns = 10, 10
        self._square_size = 40
        self._square_color = (255, 0, 0)

    def draw(self, pygame_display_surf):

        for i_row in range(self._n_rows):
            for i_col in range(self._n_columns):
                pygame.draw.rect(pygame_display_surf, self._square_color,
                                 (i_row * self._square_size,
                                  i_col * self._square_size,
                                  self._square_size,
                                  self._square_size), 2)
