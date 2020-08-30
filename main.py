import pygame
from pygame.locals import *
from grid import *
from global_constants import *
from checkbox import Checkbox
import config

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

        self.checkbox_use_corner_rule = None
        self.checkbox_use_center_rule = None
        self.checkbox_draw_total_lines_hit = None
        self.checkbox_draw_max_lines_from_single_corner = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.Grid = Grid(self._display_surf)
        self._running = True
        self._display_surf.fill(rgb_white)
        self.Grid.draw_all_tiles()

        global default_font
        default_font = pygame.font.SysFont("comicsansms", size=16)

        # config buttons
        self.checkbox_use_corner_rule = Checkbox(500, 300, "Use corner to corner rule", default_font,
                                                 checked=config.use_rule_corner_to_corner)
        self.checkbox_use_corner_rule.update()

        self.checkbox_use_center_rule = Checkbox(500, 350, "Use center to center rule", default_font,
                                                 checked=config.use_rule_center_to_center)
        self.checkbox_use_center_rule.update()

        self.checkbox_draw_total_lines_hit = Checkbox(500, 400, "Show number lines of sight hit",
                                                      default_font, checked=config.draw_text_n_lines_hit_this_tile)
        self.checkbox_draw_total_lines_hit.update()

        self.checkbox_draw_max_lines_from_single_corner = Checkbox(400, 450,
                                                                   "Show number lines of sight from single corner",
                                                                   default_font,
                                                                   checked=config.draw_text_n_max_lines_hit_this_tile_from_single_corner)
        self.checkbox_draw_max_lines_from_single_corner.update()

        # title
        pygame.display.set_caption("Descent Line of Sight Checker!")

        # legend
        self._text_hero_surface = default_font.render("Hero position (left mouse button)", True, rgb_blue)
        self._display_surf.blit(self._text_hero_surface, (self.width - 300, 100))

        self._text_monster_surface = default_font.render("Monster position (middle mouse button)", True, rgb_red)
        self._display_surf.blit(self._text_monster_surface, (self.width - 300, 150))

        self._text_obstacle_surface = default_font.render("Obstacle position (right mouse button)", True, rgb_black)
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

        if self.checkbox_use_corner_rule.on_checkbox(mouse_pos):
            self.checkbox_use_corner_rule.change_state()
            self.checkbox_use_corner_rule.update()

            config.use_rule_corner_to_corner = self.checkbox_use_corner_rule.is_checked()
            self.Grid.recompute_los()

        if self.checkbox_use_center_rule.on_checkbox(mouse_pos):
            self.checkbox_use_center_rule.change_state()
            self.checkbox_use_center_rule.update()

            config.use_rule_center_to_center = self.checkbox_use_center_rule.is_checked()
            self.Grid.recompute_los()

        if self.checkbox_draw_total_lines_hit.on_checkbox(mouse_pos):
            self.checkbox_draw_total_lines_hit.change_state()
            self.checkbox_draw_total_lines_hit.update()

            config.draw_text_n_lines_hit_this_tile = self.checkbox_draw_total_lines_hit.is_checked()
            self.Grid.draw_all_tiles()

        if self.checkbox_draw_max_lines_from_single_corner.on_checkbox(mouse_pos):
            self.checkbox_draw_max_lines_from_single_corner.change_state()
            self.checkbox_draw_max_lines_from_single_corner.update()

            config.draw_text_n_max_lines_hit_this_tile_from_single_corner = self.checkbox_draw_max_lines_from_single_corner.is_checked()
            self.Grid.draw_all_tiles()

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
