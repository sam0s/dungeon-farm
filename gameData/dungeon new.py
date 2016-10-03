import pygame
import dpylib
import math,random
from pygame import *
from os import mkdir
DISPLAY = (800, 640)
DEPTH = 16
FLAGS = pygame.RESIZABLE

##

screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.init()
display.set_caption("Dungeon Farm")
timer = pygame.time.Clock()

ent = pygame.sprite.Group()

#Connect Player and World
hud = Surface((800,128))

w=dpylib.World(ent,screen,hud)



playerName="sanm" 

def main():
    TFPS=120 #this will be an option
    w.SetLevel(playerName+"\\TestDungeon")
    w.SetPlayer(playerName)
    
    try:
        #load player attributes
        f=open(playerName+"\\"+playerName+".txt",'r')
        n=f.read()
        n=n.split("\n")
        f.close()
        

        p=dpylib.Player(int(n[5].split("_")[1]),int(n[6].split("_")[1]),w)
        w.player=p
        w.player.hp=int(n[3].split("_")[1])
        


        
        #load level

        wx=n[7].split("_")[1]
        wy=n[8].split("_")[1]
        print wx
        print wy
        dpylib.loadlvl(ent,w.levelname+"\\world"+wx+wy+".txt")

    except:

        #try to grab/create the level folder
        try:
            mkdir(w.levelname.split("\\")[0])
            mkdir(w.levelname)
            f=open(playerName+"\\"+playerName+".txt",'w')
            f.write("level_1\nbasedmg_10\nbasedef_10\nhealth_100\ngold_0\nposx_384\nposy_224")
            f.close()

        except:
            mkdir(w.levelname.split("\\")[0])
            mkdir(w.levelname)


        p=dpylib.Player(384.0,224.0,w)
        w.player=p
        
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
        display.set_caption("Dungeon Farm - "+str(timer.get_fps()))
    pygame.display.quit()
    


if(__name__ == "__main__"):
    main()
