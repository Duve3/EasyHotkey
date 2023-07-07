import pygame
from util import Button, InputField, createFont, prompt_file
import constants


class MainMenu:
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        self.res = (res[0], res[1])
        self.screen = display
        self.fpsClock = fpsClock
        self.gameFPS = fps
        self.FileLocationOutline = pygame.Rect((20, 50), (900, 50))
        self.FLFont = createFont(constants.white, 25, "./assets/CourierPrimeCode-Regular.ttf")
        buttonPos = (self.FileLocationOutline.x + (self.FileLocationOutline.w + 20), self.FileLocationOutline.y)
        buttonSize = (125, self.FileLocationOutline.height)
        buttonFont = createFont(constants.white, 30, "./assets/CourierPrimeCode-Regular.ttf")
        self.FileButton = Button(buttonPos, buttonSize, buttonFont, "browse", constants.whiteGray, constants.white, width=3, rounding=5)
        self.FONT_FileToParse = createFont(constants.white, 40, "./assets/CourierPrimeCode-Regular.ttf")
        self.directoryToScript = ""


    def run(self) -> None:  # noqa:E303
        while True:
            self.fpsClock.tick(self.gameFPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            self.FileButton.handleEvents(events)
            for event in events:
                if event.type == pygame.QUIT:
                    return

            self.screen.fill(constants.black)

            if self.FileButton.triggered:
                self.directoryToScript = prompt_file()
                self.FileButton.triggered = False

            # rendering
            pygame.draw.rect(self.screen, constants.white, self.FileLocationOutline, 3, 5)
            self.FLFont.render_to(self.screen, (self.FileLocationOutline.x + 10, self.FileLocationOutline.y + 15), self.directoryToScript)
            self.FileButton.draw(self.screen, offsets=(2, 14))

            pygame.display.flip()
