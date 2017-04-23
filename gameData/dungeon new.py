import pygame,sys
from pygame import *

DISPLAY = (800, 640)
FLAGS = HWSURFACE | DOUBLEBUF
MASTER_SURFACE = display.set_mode(DISPLAY, FLAGS, 0)

import math,random

import assets.world as world
import assets.player as player
import assets.dpylib as dl
import assets.items as items
import assets.mainmenu as mainmenu


from os import mkdir,path





##set up stuff for gameworld



screen = pygame.Surface((800,640))

pygame.init()
display.set_caption("Dungeon Farm")
timer = pygame.time.Clock()

ent = pygame.sprite.Group()


#Connect Player and World
hud = Surface((800,128))
w=world.World(ent,screen,hud)


playername="playername"




def main():
    TFPS=999 #this will be an option
    w.SetLevel(path.join(playername,"TestDungeon"))
    w.SetPlayer(playername)

    if path.isfile(path.join(playername,playername+".txt")):
        #load player attributes
        f=open(path.join(playername,playername+".txt"),'r')
        n=f.read()

        n=n.split(".")

        f.close()


        p=player.Player(int(n[7]),int(n[8]),w)
        w.player=p
        #set attributes 4=gold
        #level,xp,nextxp,hp,maxhp,atk,gold,movespeed
        p.setAttrs(n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[11])


        #loading inventory
        f=open(path.join(playername,"inv.txt"),'r')
        n2=f.read()
        f.close()

        #divide up by item
        n2=n2.split(".")
        if n2[0]!='':
            for f in n2:
                #divide up by name and stack
                f2=f.split("_")
                #give the item
                for f3 in range(int(f2[1])):
                    print f3
                    print f2
                    it=items.fromId(int(f2[0]),p)
                    print it
                    p.giveItem(it)


        #load level
        wx=n[9]
        wy=n[10]
        w.pos=[int(wx),int(wy)]

        dl.loadlvl(ent,path.join(w.levelname,"world"+wx+wy+".txt"))

    else:
        mkdir(playername)
        mkdir(w.levelname)
        p=player.Player(384.0,224.0,w)
        w.player=p

        dl.fill(ent)
        dl.carve(ent)
        dl.doors(ent)
        dl.savelvl(ent,path.join(w.levelname,"world"+str(w.pos[0])+str(w.pos[1])+".txt"),w)
    w.mouse=dl.Mouse(0,0,w)
    go=True
    while w.go:
        dt=float(timer.tick(TFPS)*1e-3)
        w.Update(dt)
        display.set_caption("Dungeon Farm - "+str(timer.get_fps()))
        MASTER_SURFACE.blit(w.surf,(0,0))
    pygame.display.quit()



if(__name__ == "__main__"):
    main()

dl.savelvl(w.containing,path.join(w.levelname,"world"+str(w.pos[0])+str(w.pos[1])+".txt"),w)
