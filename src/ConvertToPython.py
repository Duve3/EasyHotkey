import pygame
from utility.util import Button, createFont, prompt_file, BetterFont, MenuResponses, FileSelector
import utility.constants as constants
from SHKFileParser import parse
import json
from utility.menus import Menu


class PythonConvertMenu(Menu):
    def __init__(self, display: pygame.Surface, fpsClock: pygame.time.Clock, fps, res):
        super().__init__(display, fpsClock, fps, res)
        # SHK file stuff
        self.INPUT_FileSelector = FileSelector((20, 200), 900, constants.white, constants.white, 125, constants.whiteGray, constants.white, "SHK File: ", ButtonWidth=3, rounding=5)
        self.INPUT_directoryToScript = ""

        # output file stuff
        self.OUTPUT_FileSelector = FileSelector((20, self.INPUT_FileSelector.FileLocationOutline.y + 150), self.INPUT_FileSelector.FileLocationOutline.width, constants.white, constants.white, 125, constants.whiteGray, constants.white, "Result File: ", ButtonWidth=3, rounding=5)
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

        font = BetterFont(constants.white, 50, "./assets/CourierPrimeCode-Regular.ttf")
        self.BUTTON_back = Button((5, 5), (150, 50), font, "BACK", constants.whiteGray, constants.white, width=3, rounding=5)

        self.autoCode = {pygame.K_PERIOD: False, pygame.K_SLASH: False, pygame.K_f: False}
        self.hasRun = False



    def run(self) -> MenuResponses:  # noqa:E303
        while True:
            self.fpsClock.tick(self.gameFPS)

            events = pygame.event.get()  # so that we can hook into other event handlers if needed.
            # event hooking
            self.INPUT_FileSelector.handle_events(events)
            self.INPUT_directoryToScript = self.INPUT_FileSelector.directoryToFile
            triggered = self.OUTPUT_FileSelector.handle_events(events, HandleTrigger=False)
            self.convertButton.handleEvents(events)
            self.BUTTON_back.handleEvents(events)

            # event handling
            for event in events:
                if event.type == pygame.QUIT:
                    return MenuResponses.QUIT

                if event.type == pygame.KEYDOWN:
                    if event.key in self.autoCode.keys():
                        self.autoCode[event.key] = True

            # implemented in order to save me time when debugging simple changes in the file parser
            if self.hasRun is False and all(val is True for val in self.autoCode.values()):
                self.INPUT_directoryToScript = r"C:\Users\laksh\PycharmProjects\EasyHotkey\scripts\advancedStarter.ehk"
                self.OUTPUT_DirectoryToFile = r"C:\Users\laksh\PycharmProjects\EasyHotkey\scripts\test.py"
                self.INPUT_FileSelector.directoryToFile = self.INPUT_directoryToScript
                self.OUTPUT_FileSelector.directoryToFile = self.OUTPUT_DirectoryToFile
                self.convertButton.triggered = True
                self.hasRun = True

            self.screen.fill(constants.black)

            if triggered:
                self.OUTPUT_DirectoryToFile = prompt_file(savedialog=True, filetypes=[("Python Script", "*.py")])
                if self.OUTPUT_DirectoryToFile.count(".py") < 1:
                    self.OUTPUT_DirectoryToFile += ".py"
                self.OUTPUT_FileSelector.directoryToFile = self.OUTPUT_DirectoryToFile

            if self.convertButton.triggered:
                try:
                    if self.OUTPUT_DirectoryToFile != "" and self.INPUT_directoryToScript != "":
                        try:
                            with open(self.INPUT_directoryToScript) as inputFile:
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

                except Exception as exception:  # noqa:broad_exception
                    print(exception)
                    reason = self.BUFFER_Error if self.BUFFER_Error != "" else "UNKNOWN"
                    self.convertStatus = f"Status:\nFailed (E:{self.errors[reason]})"
                    self.BUFFER_Error = ""  # reset the buffer
                    self.FONT_Convert.ColorList = [constants.white, constants.red]  # make sure its white then red color list

                self.convertButton.triggered = False

            if self.BUTTON_back.triggered:
                return MenuResponses.EnterMainMenu

            # rendering
            # SHK file
            self.INPUT_FileSelector.render_to(self.screen)

            # output file
            self.OUTPUT_FileSelector.render_to(self.screen)

            # other
            self.convertButton.draw(self.screen, offsets=(2, 10))
            pygame.draw.rect(self.screen, constants.white, self.RECT_Convert, 3, 5)
            self.FONT_Convert.multiline_render_to(self.screen, (10, self.RECT_Convert.y + 22), self.convertStatus)

            self.FONT_TopText.render_to(self.screen, (self.FONT_TopText.get_center(self.screen, "SHK -> Python Menu", x=True).x, 40), "SHK -> Python Menu")
            self.BUTTON_back.draw(self.screen, offsets=(2, 10))

            pygame.display.flip()
