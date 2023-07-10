from typing import Optional
import pygame.freetype
from pygame import Surface
import tkinter
import tkinter.filedialog
from typing import Sequence, Tuple, Union

from pygame import Color
from pygame import Vector2

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

# This typehint is used when a function would return an RGBA tuble
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

STYLE_DEFAULT = pygame.freetype.STYLE_DEFAULT


def createFont(color: Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]], size: Union[float, Tuple[float, float]], fontLocation: str):
    """
    Outdated func for easily creating fonts, please use the class BetterFont if you can.
    Creates a pygame.freetype.font and sets the color and size for you
    :param color: Any color supported by pygame - anything that follows this: typing.Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
    :param size: Just and int for the size value
    :param fontLocation: the location of the .ttf or similar font file
    :return: pygame.freetype.Font
    """
    font = pygame.freetype.Font(fontLocation, size=size)
    font.fgcolor = color
    return font


# btw if something isnt type checked (doesnt have the arg: thing) its probably in the util.pyi file.
class BetterFont(pygame.freetype.Font):
    def __init__(self, fgColor: Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]], fontSize: Union[float, Tuple[float, float]], location: str, font_index: int = 0, resolution: int = 0, ucs4: int = False):
        super().__init__(location, size=fontSize, font_index=font_index, resolution=resolution, ucs4=ucs4)
        self.fgcolor = fgColor

    def multiline_render_to(self, surf: Surface, dest, text: str, fgcolor: Optional[ColorValue] = None, bgcolor: Optional[ColorValue] = None, style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0) -> list[pygame.rect.Rect]:
        ListText = text.splitlines()
        ListRects = []
        for i, line in enumerate(ListText):
            rect = self.render_to(surf=surf, dest=(dest[0], dest[1] + (i * self.size + 10)), text=line, fgcolor=fgcolor, bgcolor=bgcolor, style=style, rotation=rotation, size=size)
            ListRects.append(rect)

        return ListRects

    # probably works idk
    def multiline_render(self, text: str, fgcolor: Optional[ColorValue] = None, bgcolor: Optional[ColorValue] = None, style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0,) -> list[Tuple[Surface, pygame.rect.Rect]]:
        ListText = text.splitlines()
        ListSurfs = []
        for i, line in enumerate(ListText):
            surfRect = self.render(text=line, fgcolor=fgcolor, bgcolor=bgcolor, style=style, rotation=rotation, size=size)
            ListSurfs.append(surfRect)

        return ListSurfs


class InputField:
    def __init__(self, pos, size, activeColor, unactiveColor, font, placeholderFont, charLimit: int = 20, surfaceOffset=(0, 0), placeHolderText=""):
        self.x = pos[0]
        self.y = pos[1]
        self.active = False
        self.rect = pygame.Rect(pos, size)
        self.text = ""
        self.ColorActive = activeColor
        self.ColorUnactive = unactiveColor
        self.color = self.ColorUnactive
        self.charLimit = charLimit
        self.font = font
        self.FONTPlaceholder = placeholderFont
        self.placeholderText = placeHolderText
        self.surfaceOffset = surfaceOffset

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                if self.rect.collidepoint(mx, my):
                    self.active = True
                else:
                    self.active = False

            elif event.type == pygame.KEYDOWN and self.active:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    self.text = self.text[:-1]

                # Unicode standard is used for string
                # formation
                elif len(self.text) < self.charLimit:
                    self.text += event.unicode

        if self.active:
            self.color = self.ColorActive
        else:
            self.color = self.ColorUnactive

    def draw(self, screen, offsets=(5, 5)):
        self.rect = pygame.Rect((self.x, self.y), (self.rect.w, self.rect.h))
        pygame.draw.rect(screen, self.color, self.rect)
        if len(self.text) <= 0:
            self.FONTPlaceholder.render_to(screen, ((self.rect.centerx - self.FONTPlaceholder.get_rect(self.placeholderText, size=self.FONTPlaceholder.size).centerx) + offsets[0], self.y + offsets[1]), self.placeholderText)
        else:
            self.font.render_to(screen, ((self.rect.centerx - self.font.get_rect(self.text, size=self.font.size).centerx) + offsets[0], self.y + offsets[1]), self.text)


class Button:
    def __init__(self, pos, size, font, text, activeColor, unactiveColor, surfaceOffsets=(0, 0), width: int = 0, rounding: int = -1):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = font
        self.text = text
        self.color = unactiveColor
        self.activeColor = activeColor
        self.unactiveColor = unactiveColor
        self.triggered = False
        self.hovered = False
        self.surfaceOffset = surfaceOffsets
        self.width = width
        self.rounding = rounding

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                self.triggered = self.rect.collidepoint(mx, my)

            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                self.hovered = self.rect.collidepoint(mx, my)

    def draw(self, screen, offsets=(5, 5)):
        self.rect = pygame.Rect((self.x, self.y), (self.rect.w, self.rect.h))
        self.color = self.unactiveColor if not self.hovered else self.activeColor
        pygame.draw.rect(screen, self.color, self.rect, self.width, self.rounding)
        self.font.fgcolor = self.color
        self.font.render_to(screen, ((self.rect.centerx - self.font.get_rect(self.text, size=self.font.size).centerx) + offsets[0], self.y + offsets[1]), self.text)


def prompt_file(filetypes: list = None, savedialog=False):
    """Create a Tk file dialog and cleanup when finished"""
    if filetypes is None:
        filetypes = [("EasyHotkey Files", "*.ehk")]
    top = tkinter.Tk()
    top.withdraw()  # hide window
    if not savedialog:
        file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=filetypes)
    else:
        file_name = tkinter.filedialog.asksaveasfilename(parent=top, filetypes=filetypes)
    top.destroy()
    return file_name
