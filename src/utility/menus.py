import pygame
from .util import MenuResponses


class Menu:
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        self.res = (res[0], res[1])
        self.screen = display
        self.fpsClock = fpsClock
        self.gameFPS = fps

    def run(self) -> MenuResponses: ...  # self defined function

    def reset(self):
        self.__init__(self.screen, self.fpsClock, self.gameFPS, self.res)
