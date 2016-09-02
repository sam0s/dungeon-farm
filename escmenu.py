#################################
# sam0s #######################
#################################


import pygame
from random import choice
from pygame import *
import dpylib
import ui


pygame.init()
font=pygame.font.Font(None,15)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Square(Entity):
    def __init__(self,x,y,c):
        Entity.__init__(self)
        self.image=pygame.Surface((6,6))
        self.image.fill(c)
        self.rect=(x/6,y/6,5,5)
    

class EscMenu(object):
    def __init__(self,surf,world):
        self.surf=surf
        self.world=world
        self.small = pygame.sprite.Group()
        self.small2 = pygame.sprite.Group()
        
        self.created=0
        self.buttons=[ui.Button(300,300,100,32,"Go Back.",self.surf)]
        #self.CreateSmallMap(str(self.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small)
    def CreateSmallMap(self,loc,lev,offset=0,offsety=0):
        #self.small.empty()
        FNF=0
        try:
            load = open(loc,"r")
        except:
            FNF=1
        if FNF==0:
            read = 0
            data = load.read()
            data=data.split(".")
            data=data[:-1]
            
            while len(data) > 0:
                c=(0,0,0)
                if data[0]=='"wall"':
                    c=(100,100,100)
                lev.add(Square(int(data[1])+offset,int(data[2])+offsety,c))
                data=data[3:]
            load.close()
            lev.add(Square(self.world.player.rect.x+792,self.world.player.rect.y+492,(0,255,0)))
    def Draw(self):
        self.surf.fill((0,0,250))

        if self.world.good==1:
            if self.world.keys[K_ESCAPE]:
                self.world.ChangeState("game")
                
        
        if not self.world.keys[K_ESCAPE]:
            self.world.good=1
    
        
        for e in self.world.events:
            #button handling
            if e.type == MOUSEBUTTONUP:
                for b in self.buttons:
                    if b.rect.collidepoint(e.pos):
                        self.world.ChangeState("game")
            if e.type == QUIT:
                dpylib.savelvl(self.world.containing,self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt")
                self.world.go = False

        if self.created==0:
            self.small.empty()

            #top
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]-1)+str(self.world.pos[1]-1)+".txt"),self.small,0)
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1]-1)+".txt"),self.small,792)
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]+1)+str(self.world.pos[1]-1)+".txt"),self.small,1584)
            
            #mid
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]-1)+str(self.world.pos[1])+".txt"),self.small,0,492)
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small,792,492)
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]+1)+str(self.world.pos[1])+".txt"),self.small,1584,492)
            

            #bot
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]-1)+str(self.world.pos[1]+1)+".txt"),self.small,0,984)
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1]+1)+".txt"),self.small,792,984)
            self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]+1)+str(self.world.pos[1]+1)+".txt"),self.small,1584,984)

            self.created=1
        else:
            self.small.draw(self.surf)


        for f in self.buttons:
            f.Update()

            
            
            
        
