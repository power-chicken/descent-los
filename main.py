import pygame
from pygame.locals import *
from grid import *

white = (255, 255, 255)
red = (255, 0, 0)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 500
        self.Grid = None
        self.clock = pygame.time.Clock()
        self._fps = 3

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.Grid = Grid()
        self._running = True
        self._display_surf.fill(white)
        self.Grid.draw(self._display_surf)

        pygame.display.set_caption("Descent Line of Sight Checker!")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_lbutton_down(event)
            elif event.button == 2:
                self.on_mbutton_down(event)
            elif event.button == 3:
                self.on_rbutton_down(event)

    def on_lbutton_down(self, event):
        print("l")
    def on_mbutton_down(self, event):
        print("m")
    def on_rbutton_down(self, event):
        print("r")

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
