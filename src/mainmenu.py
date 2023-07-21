import pygame
from utility.util import MenuResponses
from utility.menus import Menu


class MainMenu(Menu):
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        super().__init__(display, fpsClock, fps, res)



    def run(self) -> MenuResponses:  # noqa:E303
        while True:
            self.fpsClock.tick(self.gameFPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            # event handling
            for event in events:
                if event.type == pygame.QUIT:
                    return MenuResponses.QUIT

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return MenuResponses.EnterPCMMenu
                    elif event.key == pygame.K_2:
                        return MenuResponses.EnterExecuteMenu

            pygame.display.flip()
