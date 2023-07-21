from utility.menus import Menu
from utility.util import FileSelector, MenuResponses, BetterFont
import utility.constants as constants
import pygame
from SHKFileParser import parse


class SHKScript:
    def __init__(self, pathToScript: str):
        # if this raises an error thats your fault not mine
        with open(pathToScript, "r") as f:
            self.script = f.read()

        self.pyhk = parse(self.script)

    def execute(self):
        exec(self.pyhk)  # this can create UB and has security flaws, but its easiest way to do it.


class ExecuteMenu(Menu):
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res) -> None:
        super().__init__(display, fpsClock, fps, res)

        # path to the script for execution
        self.scriptPath = ""
        self.executeFileSelector = FileSelector((20, 200), 900, constants.white, constants.white, 125, constants.whiteGray, constants.white, "SHK File: ", ButtonWidth=3, rounding=5)

        # other
        self.FONT_TopText = BetterFont(constants.white, 50, "./assets/CourierPrimeCode-Regular.ttf")


    def run(self) -> MenuResponses:  # noqa:line_sep
        while True:
            self.fpsClock.tick(self.gameFPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            # event hooking
            self.executeFileSelector.handle_events(events)
            # event handling
            for event in events:
                if event.type == pygame.QUIT:
                    return MenuResponses.QUIT

            # logic


            # rendering
            self.screen.fill(constants.black)
            self.executeFileSelector.render_to(self.screen)

            self.FONT_TopText.render_to(self.screen, (self.FONT_TopText.get_center(self.screen, "SHK Execution Menu", x=True).x, 40), "SHK Execution Menu2")

            pygame.display.flip()
