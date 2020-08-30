import pygame


class Checkbox:

    def __init__(self, x, y, text, font, checked=False):
        self.screen = pygame.display.get_surface()
        self.checked = checked
        self.text = text

        self.checkboxRect = pygame.Rect(x, y, 15, 15)
        self.crossRect = pygame.Rect(x + 2, y + 2, 11, 11)

        if pygame.font:
            self.text_disp = font.render(self.text, 1, (75, 75, 75))

        self.textRect = self.text_disp.get_rect(x=x + 25, centery=y + 9)

        self.screen.blit(self.text_disp, self.textRect)
        self.update()

    def update(self):
        pygame.draw.rect(self.screen, (150, 150, 150), self.checkboxRect)

        if self.checked:
            pygame.draw.rect(self.screen, (75, 75, 75), self.crossRect)

    def on_checkbox(self, position):
        if self.get_x() <= position[0] <= (self.get_x() + 25 + self.textRect.w) and \
                self.get_y() <= position[1] <= (self.get_y() + 15):
            return True
        else:
            return False

    def change_state(self):
        if self.is_checked():
            self.uncheck()
        else:
            self.check()

        self.update()

        return self.is_checked()

    def is_checked(self):
        return self.checked

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def get_x(self):
        return self.checkboxRect.x

    def get_y(self):
        return self.checkboxRect.y
