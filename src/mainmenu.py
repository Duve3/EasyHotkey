import pygame
from utility.util import MenuResponses


class MainMenu:
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        self.res = (res[0], res[1])
        self.screen = display
        self.fpsClock = fpsClock
        self.gameFPS = fps



    def run(self) -> MenuResponses:  # noqa:E303
        while True:
            self.fpsClock.tick(self.gameFPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            # event handling
            for event in events:
                if event.type == pygame.QUIT:
                    return MenuResponses.QUIT

            pygame.display.flip()
