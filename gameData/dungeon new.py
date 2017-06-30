import pygame,sys,json
from os import path
from pygame import *

DISPLAY = (800, 640)
FLAGS = HWSURFACE | DOUBLEBUF
MASTER_SURFACE = display.set_mode(DISPLAY, FLAGS, 0)

import assets.game as game

screen = pygame.Surface((800,640))

pygame.init()
display.set_caption("Dungeon Farm [800x640]")

timer = pygame.time.Clock()
GAME = game.Game(screen)

def main2():
    while GAME.go:
        GAME.Update(dt=float(timer.tick(999)*1e-3))
        display.set_caption("Dungeon Farm - "+str(timer.get_fps()))
        MASTER_SURFACE.blit(GAME.surf,(0,0))

if(__name__ == "__main__"):
    main2()
