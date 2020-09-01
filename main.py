from grid import TileGrid
from global_constants import *
from checkbox import Checkbox
import config
import kivy
from kivy.app import App as KivyApp
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

default_font = None


class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)

        self.cols = 1

        self.tile_grid = TileGrid()

        self.add_widget(self.tile_grid)

        self.add_widget(Label(text="name"))

        self.test_button = Button(text="arsch", font_size=default_font_size)
        self.test_button.bind(on_press=self.press_test_button)
        self.add_widget(self.test_button)

    def press_test_button(self, instance):
        print("pressed button")


class LosCheckerApp(KivyApp):

    def __init__(self):

        super().__init__()

        self.main_grid = MainGrid()

        self._text_hero_surface = None
        self._text_monster_surface = None
        self._text_obstacle_surface = None

        self.checkbox_use_corner_rule = None
        self.checkbox_use_center_rule = None

        self.checkbox_draw_total_lines_hit = None
        self.checkbox_draw_lines_from_single_corner = None
        self.checkbox_draw_los_square = None
        self.checkbox_draw_defense_bonus = None

    def build(self):
        return self.main_grid

    def on_init(self):

        # config buttons
        self.checkbox_use_corner_rule = Checkbox(500, 300, "Use corner to corner rule", default_font,
                                                 checked=config.use_rule_corner_to_corner)
        self.checkbox_use_center_rule = Checkbox(500, 350, "Use center to center rule", default_font,
                                                 checked=config.use_rule_center_to_center)
        self.checkbox_draw_total_lines_hit = Checkbox(500, 400, "Show number lines of sight hit",
                                                      default_font, checked=config.draw_text_n_lines_hit_this_tile)
        self.checkbox_draw_lines_from_single_corner = Checkbox(400, 450,
                                                               "Show number lines of sight from single corner",
                                                               default_font,
                                                               checked=config.draw_text_lines_hit_from_single_corner)
        self.checkbox_draw_los_square = Checkbox(400, 500,
                                                 "Draw los square",
                                                 default_font,
                                                 checked=config.draw_los_square)
        self.checkbox_draw_defense_bonus = Checkbox(400, 550,
                                                    "Draw defense bonus",
                                                    default_font,
                                                    checked=config.draw_defense_bonus)

        # legend
        self._text_hero_surface = default_font.render("Hero position (left mouse button)", True, rgb_blue)

        self._text_monster_surface = default_font.render("Monster position (middle mouse button)", True, rgb_red)

        self._text_obstacle_surface = default_font.render("Obstacle position (right mouse button)", True, rgb_black)

    def on_left_button_down(self, event):

        if self.checkbox_use_corner_rule.on_checkbox(mouse_pos):
            config.use_rule_corner_to_corner = self.checkbox_use_corner_rule.change_state()
            self.Grid.recompute_los()

        elif self.checkbox_use_center_rule.on_checkbox(mouse_pos):
            config.use_rule_center_to_center = self.checkbox_use_center_rule.change_state()
            self.Grid.recompute_los()

        elif self.checkbox_draw_total_lines_hit.on_checkbox(mouse_pos):
            config.draw_text_n_lines_hit_this_tile = self.checkbox_draw_total_lines_hit.change_state()

        elif self.checkbox_draw_lines_from_single_corner.on_checkbox(mouse_pos):
            config.draw_text_lines_hit_from_single_corner = self.checkbox_draw_lines_from_single_corner.change_state()

        elif self.checkbox_draw_los_square.on_checkbox(mouse_pos):
            config.draw_los_square = self.checkbox_draw_los_square.change_state()

        elif self.checkbox_draw_defense_bonus.on_checkbox(mouse_pos):
            config.draw_defense_bonus = self.checkbox_draw_defense_bonus.change_state()

        else:
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


if __name__ == "__main__":

    LosCheckerApp().run()
