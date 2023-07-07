from EHKFileParser import parse
import pygame
import ctypes
from mainmenu import MainMenu


# pygame yahoo
def main():
    myappid = u'alterra.software.easyhotkey.main'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    pygame.init()

    RES = (1080, 720)  # idek what resolution this is
    pygame.display.set_caption("Easy Hotkey (EHK)")
    window = pygame.display.set_mode(RES)
    fpsClock = pygame.time.Clock()
    fps = 60
    mm = MainMenu(window, fpsClock, fps, RES)
    mm.run()


if __name__ == "__main__":
    main()

    # since the pygame interface is currently not working, please just uncomment the code below when actually using EHK.
    # directoryToFile = input("What's the exact directory to the file you are converting? ")
    #
    # with open(directoryToFile) as f:
    #     pyhk = parse(f.read())
    #
    # print(pyhk)


