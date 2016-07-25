import pygame
import dpylib
import math,random
from pygame import *
from os import mkdir
DISPLAY = (800, 640)
DEPTH = 32
FLAGS = 0

levelname="lvl"

screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.init()
display.set_caption("DungeonPy")
timer = time.Clock()

ent = pygame.sprite.Group()
ent.add(dpylib.Player(0,0))
hud = Surface((800,128))


def main():

    worldpos = [0,0]
    try:
        dpylib.loadlvl(ent,levelname+"\\world00.txt")
    except:
        mkdir(levelname)
        dpylib.fill(ent)
        dpylib.carve(ent)
    go=True

    while go:
        dt=timer.tick(60)
        speed = 1 / float(dt)
        speed = 5 * speed
        screen.fill((0,0,0))

        for e in pygame.event.get():
            if e.type == QUIT:
                dpylib.savelvl(ent,levelname+"\\world"+str(worldpos[0])+str(worldpos[1])+".txt")
                go = False
            if e.type == KEYUP:
                dpylib.savelvl(ent,levelname+"\\world"+str(worldpos[0])+str(worldpos[1])+".txt")
                if e.key==K_RIGHT:
                    worldpos[0]+=1
                if e.key==K_LEFT:
                    worldpos[0]-=1
                if e.key==K_UP:
                    worldpos[1]-=1
                if e.key==K_DOWN:
                    worldpos[1]+=1
                dpylib.changelevel(ent,levelname,worldpos)

        ent.draw(screen)
        dpylib.drawhud(hud)
        screen.blit(hud, (0,512))
        pygame.display.flip()
        display.set_caption("DungeonPy - "+str(speed))

if(__name__ == "__main__"):
    main()
