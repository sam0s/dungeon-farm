import pygame
import dpylib
import math,random
from pygame import *
from os import mkdir
DISPLAY = (800, 640)
DEPTH = 16
FLAGS = pygame.RESIZABLE



screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.init()
display.set_caption("DungeonPy")
timer = pygame.time.Clock()

ent = pygame.sprite.Group()

#Connect Player and World
hud = Surface((800,128))

w=dpylib.World(ent,screen,hud)
p=dpylib.Player(384.0,224.0,w)
w.player=p

def main():
    TFPS=120 #this will be an option
    w.SetLevel("Cool Level Name")
    print w.levelname
    try:
        dpylib.loadlvl(ent,w.levelname+"\\world00.txt")
    except:

        #try to grab/create the level folder
        try:
            mkdir(w.levelname)
        except:
            pass
        
        dpylib.fill(ent)
        dpylib.carve(ent)
        dpylib.doors(ent)
        dpylib.savelvl(ent,w.levelname+"\\world"+str(w.pos[0])+str(w.pos[1])+".txt")
    go=True
    w.Draw()
    pygame.display.flip()
    while w.go:
        #mse=pygame.mouse.get_pos()
        #mse=(((mse[0])/32)*32,((mse[1])/32)*32)
        
        #speed = 1 / float(dt)
        #speed = 5 * speed
        #screen.fill((0,0,0))
        
        dt=float(timer.tick(TFPS)*1e-3)
        #dst=timer.tick(TFPS)
        #dt=1/float(dst)
        #print dt
        w.Update(dt)
        display.set_caption("DungeonPy - "+str(timer.get_fps()))
    pygame.display.quit()
    


if(__name__ == "__main__"):
    main()
