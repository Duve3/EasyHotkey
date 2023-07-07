import pygame
from util import Button, InputField


class MainMenu:
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        self.res = (res[0], res[1])
        self.screen = display
        self.fpsClock = fpsClock
        self.FPS = fps


    def run(self) -> None:  # noqa:E303
        while True:
            self.fpsClock.tick(self.FPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            for event in events:
                if event.type == pygame.QUIT:
                    return
