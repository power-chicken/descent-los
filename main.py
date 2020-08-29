import pygame
from pygame.locals import *
from grid import *
from global_constants import *
from checkbox import Checkbox


default_font = None


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 500
        self.Grid = None
        self.clock = pygame.time.Clock()
        self._fps = 15

        self._text_hero_surface = None
        self._text_monster_surface = None
        self._text_obstacle_surface = None

        self.test_checkbox = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.Grid = Grid(self._display_surf)
        self._running = True
        self._display_surf.fill(rgb_white)
        self.Grid.draw_all_tiles()

        global default_font
        default_font = pygame.font.SysFont("comicsansms", size=16)

        self.test_checkbox = Checkbox(500, 300, "hi", default_font)
        self.test_checkbox.update()

        pygame.display.set_caption("Descent Line of Sight Checker!")

        self._text_hero_surface = default_font.render("Hero position (left mouse button)", True, rgb_blue)
        self._display_surf.blit(self._text_hero_surface, (self.width - 300, 100))

        self._text_monster_surface = default_font.render("Monster position (middle mouse button)", True, rgb_red)
        self._display_surf.blit(self._text_monster_surface, (self.width - 300, 150))

        self._text_obstacle_surface = default_font.render("Obstacle position (right mouse button)", True,
                                                               rgb_black)
        self._display_surf.blit(self._text_obstacle_surface, (self.width - 300, 200))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_left_button_down(event)
            elif event.button == 2:
                self.on_middle_button_down(event)
            elif event.button == 3:
                self.on_right_button_down(event)

    def on_left_button_down(self, event):

        mouse_pos = pygame.mouse.get_pos()

        if self.test_checkbox.on_checkbox(mouse_pos):
            self.test_checkbox.change_state()
            self.test_checkbox.update()

        tile = self.Grid.get_tile_from_pixel(mouse_pos)
        self.Grid.set_tile_type(tile, 'hero')
        self.Grid.draw_all_tiles()

    def on_middle_button_down(self, event):
        tile = self.Grid.get_tile_from_pixel(pygame.mouse.get_pos())
        self.Grid.set_tile_type(tile, 'monster')
        self.Grid.draw_all_tiles()

    def on_right_button_down(self, event):
        tile = self.Grid.get_tile_from_pixel(pygame.mouse.get_pos())
        self.Grid.set_tile_type(tile, 'obstacle')
        self.Grid.draw_all_tiles()

    def on_loop(self):
        self.clock.tick(self._fps)

    def on_render(self):
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
