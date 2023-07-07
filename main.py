from customParser import parse
import pygame

if __name__ == "__main__":
    # TODO: replace with some kind of pygame script
    directoryToFile = input("Whats the exact directory to the file you are converting? ")

    with open(directoryToFile) as f:
        pyhk = parse(f.read())

    print(pyhk)
    exec(pyhk)


