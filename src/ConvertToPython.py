import pygame
from utility.util import Button, createFont, prompt_file, BetterFont
import utility.constants as constants
from SHKFileParser import parse
import json


class PythonConvertMenu:
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        self.res = (res[0], res[1])
        self.screen = display
        self.fpsClock = fpsClock
        self.gameFPS = fps
        # EHK file stuff
        self.FileLocationOutline = pygame.Rect((20, 200), (900, 50))
        self.FLFont = createFont(constants.white, 25, "./assets/CourierPrimeCode-Regular.ttf")
        buttonPos = (self.FileLocationOutline.x + (self.FileLocationOutline.w + 20), self.FileLocationOutline.y)
        buttonSize = (125, self.FileLocationOutline.height)
        buttonFont = createFont(constants.white, 30, "./assets/CourierPrimeCode-Regular.ttf")
        self.FileButton = Button(buttonPos, buttonSize, buttonFont, "browse", constants.whiteGray, constants.white, width=3, rounding=5)
        self.FONT_FileToParse = createFont(constants.white, 40, "./assets/CourierPrimeCode-Regular.ttf")
        self.directoryToScript = ""

        # output file stuff
        self.OUTPUT_FileLocationOutline = pygame.Rect((20, self.FileLocationOutline.y + 150), self.FileLocationOutline.size)
        self.OUTPUT_FLFont = createFont(constants.white, 25, "./assets/CourierPrimeCode-Regular.ttf")
        buttonPos = (self.OUTPUT_FileLocationOutline.x + (self.OUTPUT_FileLocationOutline.w + 20), self.OUTPUT_FileLocationOutline.y)
        buttonSize = (125, self.OUTPUT_FileLocationOutline.height)
        buttonFont = createFont(constants.white, 30, "./assets/CourierPrimeCode-Regular.ttf")
        self.OUTPUT_FileButton = Button(buttonPos, buttonSize, buttonFont, "browse", constants.whiteGray, constants.white, width=3, rounding=5)
        self.OUTPUT_FONT_ResultFile = createFont(constants.white, 40, "./assets/CourierPrimeCode-Regular.ttf")
        self.OUTPUT_DirectoryToFile = ""

        # other
        font = createFont(constants.white, 50, "./assets/CourierPrimeCode-Regular.ttf")
        self.convertButton = Button((self.screen.get_rect().centerx - 125, 600), (250, 50), font, "CONVERT", constants.whiteGray, constants.white, width=3, rounding=5)
        self.convertStatus = "Status:\nWaiting"
        self.RECT_Convert = pygame.Rect((-4, 550), (350, 130))
        self.FONT_Convert = BetterFont(constants.white, 40, "./assets/CourierPrimeCode-Regular.ttf", ColorList=[constants.white, constants.white])
        self.FONT_TopText = BetterFont(constants.white, 50, "./assets/CourierPrimeCode-Regular.ttf")

        with open("./ErrorCodes.json") as ecf:
            Errors = json.loads(ecf.read())
            self.errors = Errors["PythonConvertMenu"]

        self.BUFFER_Error = ""


    def run(self) -> None:  # noqa:E303
        while True:
            self.fpsClock.tick(self.gameFPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            # event hooking
            self.FileButton.handleEvents(events)
            self.OUTPUT_FileButton.handleEvents(events)
            self.convertButton.handleEvents(events)

            # event handling
            for event in events:
                if event.type == pygame.QUIT:
                    return

            self.screen.fill(constants.black)

            if self.FileButton.triggered:
                self.directoryToScript = prompt_file(savedialog=False, filetypes=[("SimpleHotkey Files", "*.shk"), ("EasyHotkey Files", "*.ehk")])
                self.FileButton.triggered = False

            if self.OUTPUT_FileButton.triggered:
                self.OUTPUT_DirectoryToFile = prompt_file(savedialog=True, filetypes=[("Python Hotkey Script", "*.pyhk")])
                if self.OUTPUT_DirectoryToFile.count(".pyhk") < 1:
                    self.OUTPUT_DirectoryToFile += ".pyhk"
                self.OUTPUT_FileButton.triggered = False

            if self.convertButton.triggered:
                try:
                    if self.OUTPUT_DirectoryToFile != "" and self.directoryToScript != "":
                        try:
                            with open(self.directoryToScript) as inputFile:
                                res = parse(inputFile.read())
                        except PermissionError:
                            self.BUFFER_Error = "READ_PERMISSION"
                        except OSError:
                            self.BUFFER_Error = "OS_ERROR"
                        except ValueError:
                            self.BUFFER_Error = "VALUE_ERROR"

                        with open(self.OUTPUT_DirectoryToFile, "w") as outputFile:
                            outputFile.write(res)
                            outputFile.truncate()

                        self.convertStatus = "Status:\nSuccess"
                        self.FONT_Convert.ColorList = [constants.white, constants.green]
                    else:
                        self.BUFFER_Error = "MISSING_FILES"
                        raise Exception  # to trigger the FAILED message

                except Exception:  # noqa:broad_exception
                    reason = self.BUFFER_Error if self.BUFFER_Error != "" else "UNKNOWN"
                    self.convertStatus = f"Status:\nFailed (E:{self.errors[reason]})"
                    self.BUFFER_Error = ""  # reset the buffer
                    self.FONT_Convert.ColorList = [constants.white, constants.red]  # make sure its white then red color list

                self.convertButton.triggered = False

            # rendering
            # SHK file
            self.FONT_FileToParse.render_to(self.screen, (30, self.FileLocationOutline.y - 40), "SHK File: ")
            pygame.draw.rect(self.screen, constants.white, self.FileLocationOutline, 3, 5)
            self.FLFont.render_to(self.screen, (self.FileLocationOutline.x + 10, self.FileLocationOutline.y + 15), self.directoryToScript)
            self.FileButton.draw(self.screen, offsets=(2, 14))

            # output file
            self.OUTPUT_FONT_ResultFile.render_to(self.screen, (30, self.OUTPUT_FileLocationOutline.y - 40), "Result File: ")
            pygame.draw.rect(self.screen, constants.white, self.OUTPUT_FileLocationOutline, 3, 5)
            self.OUTPUT_FLFont.render_to(self.screen, (self.OUTPUT_FileLocationOutline.x + 10, self.OUTPUT_FileLocationOutline.y + 15), self.OUTPUT_DirectoryToFile)
            self.OUTPUT_FileButton.draw(self.screen, offsets=(2, 14))

            # other
            self.convertButton.draw(self.screen, offsets=(2, 10))
            pygame.draw.rect(self.screen, constants.white, self.RECT_Convert, 3, 5)
            self.FONT_Convert.multiline_render_to(self.screen, (10, self.RECT_Convert.y + 22), self.convertStatus)

            self.FONT_TopText.render_to(self.screen, (self.FONT_TopText.get_center(self.screen, "SHK -> Python Menu", x=True).x, 40), "SHK -> Python Menu")

            pygame.display.flip()
