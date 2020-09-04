from grid import TileGrid
from global_constants import *
from aux_functions import get_color_by_tile_type
import config
from kivy.app import App as KivyApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class TileChangeModeButton(Button):
    def __init__(self, tile_type, box_with_other_buttons, **kwargs):
        super(TileChangeModeButton, self).__init__(**kwargs)

        self.type = tile_type
        self.text = self.type
        self.background_color = get_color_by_tile_type(self.type)

        self.box_with_other_buttons = box_with_other_buttons
        self.bind(on_press=self.press_button, on_release=self.release_button)

    def press_button(self, instance):
        self.background_color = rgb_white

    def update_text(self):
        highlight_factor = 2 if config.tile_type_change_mode == self.type else 1
        self.font_size = highlight_factor * default_font_size
        self.background_color = get_color_by_tile_type(self.type)

    def release_button(self, instance):
        config.tile_type_change_mode = self.type
        self.box_with_other_buttons.update_all_buttons_text()


class ChangeTileButtonBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ChangeTileButtonBox, self).__init__(**kwargs)

        self.button_list = [TileChangeModeButton(tile_type, self) for tile_type in tile_types]

        for button in self.button_list:
            self.add_widget(button)

    def update_all_buttons_text(self):
        for button in self.button_list:
            button.update_text()


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.orientation = "vertical"

        self.tile_grid = TileGrid()
        self.add_widget(self.tile_grid)

        self.add_widget(Label(text="hello this is a test string", size_hint_y=0.05))

        self.tile_change_mode_button_box = ChangeTileButtonBox()
        self.tile_change_mode_button_box.size_hint_y = 0.1
        self.add_widget(self.tile_change_mode_button_box)


class LosCheckerApp(KivyApp):
    def __init__(self):
        super().__init__()
        self.main_grid = MainWidget()

    def build(self):
        return self.main_grid


if __name__ == "__main__":

    LosCheckerApp().run()
