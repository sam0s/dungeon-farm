import pygame,sys
import dpylib
import math,random
from pygame import *
from os import mkdir,path
DISPLAY = (800, 640)

FLAGS = HWSURFACE | DOUBLEBUF

##


MASTER_SURFACE = display.set_mode(DISPLAY, FLAGS, 0)

screen = pygame.Surface((800,640))

pygame.init()
display.set_caption("Dungeon Farm")
timer = pygame.time.Clock()

ent = pygame.sprite.Group()

#LOAD ALL IMAGES! MAYBE A BAD IDEA
allImages=[pygame.image.load("images\\items.png").convert(),pygame.image.load("images\\menu.png").convert(),pygame.image.load("images\\headshot1.png").convert(),pygame.image.load("images\\orcheadshot.png")]


#Connect Player and World
hud = Surface((800,128))

w=dpylib.World(ent,screen,hud,allImages)




playername="sanm" 

def main():
    TFPS=999 #this will be an option
    w.SetLevel(playername+"\\TestDungeon")
    w.SetPlayer(playername)
    MASTER_SURFACE_WIDTH=800
    MASTER_SURFACE_HEIGHT=640
    if path.isfile(playername+"\\"+playername+".txt"):
        #load player attributes
        f=open(playername+"\\"+playername+".txt",'r')
        n=f.read()
        n=n.split("\n")
        f.close()
        

        p=dpylib.Player(int(n[5].split("_")[1]),int(n[6].split("_")[1]),w)
        w.player=p
        w.player.hp=int(n[3].split("_")[1])


        
        #load level
        wx=n[7].split("_")[1]
        wy=n[8].split("_")[1]
        w.pos=[int(wx),int(wy)]
        dpylib.loadlvl(ent,w.levelname+"\\world"+wx+wy+".txt")

    else:
        #e = sys.exc_info()
        #print e
        #try to grab/create the level folder
        try:
            mkdir(w.levelname.split("\\")[0])
            mkdir(w.levelname)
            f=open(playername+"\\"+playername+".txt",'w')
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
        dt=float(timer.tick(TFPS)*1e-3)
        w.Update(dt)
        display.set_caption("Dungeon Farm - "+str(timer.get_fps()))
        
        MASTER_SURFACE.blit(w.surf,(0,0))
    pygame.display.quit()
    


if(__name__ == "__main__"):
    main()
