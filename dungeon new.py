import pygame
import dpylib
import math,random
from pygame import *
from os import mkdir
DISPLAY = (800, 640)
DEPTH = 16
FLAGS = pygame.RESIZABLE

levelname="lvl"

screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.init()
display.set_caption("DungeonPy")
timer = time.Clock()

ent = pygame.sprite.Group()
p=dpylib.Player(384,224)
hud = Surface((800,128))
eggs=dpylib.Log(12,12)
print eggs
def main():
    try:
        dpylib.loadlvl(ent,levelname+"\\world00.txt")
    except:
        mkdir(levelname)
        dpylib.fill(ent)
        dpylib.carve(ent)
        dpylib.doors(ent)
    go=True

    while go:
        mse=pygame.mouse.get_pos()
        mse=(((mse[0])/32)*32,((mse[1])/32)*32)
        dt=timer.tick(60)
        #speed = 1 / float(dt)
        #speed = 5 * speed
        screen.fill((0,0,0))

        for e in pygame.event.get():
            if e.type == QUIT:
                dpylib.savelvl(ent,levelname+"\\world"+str(p.worldpos[0])+str(p.worldpos[1])+".txt")
                go = False
            
        ent.draw(screen)
        dpylib.drawhud(hud)
        screen.blit(hud, (0,512))
        p.update(screen)
        pygame.display.flip()
        display.set_caption("DungeonPy - "+str(mse))
    pygame.display.quit()

if(__name__ == "__main__"):
    main()
