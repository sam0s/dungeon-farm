#################################
# sam0s #######################
#################################


import pygame
from random import choice
from pygame import *
import dpylib


pygame.init()
font=pygame.font.Font(None,15)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Square(Entity):
    def __init__(self,x,y,c):
        Entity.__init__(self)
        self.image=pygame.Surface((8,8))
        self.image.fill(c)
        self.rect=(x/4,y/4,8,8)
    

class EscMenu(object):
    def __init__(self,surf,world,loc):
        self.surf=surf
        self.world=world
        self.levelname=loc
        self.small = pygame.sprite.Group()
        self.created=0
        #self.CreateSmallMap(str(self.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small)
    def CreateSmallMap(self,loc,lev):
        self.small.empty()
        load = open(loc,"r")
        read = 0
        data = load.read()
        data=data.split(".")
        data=data[:-1]
        
        while len(data) > 0:
            c=(0,0,0)
            if data[0]=='"wall"':
                c=(100,100,100)
            lev.add(Square(int(data[1]),int(data[2]),c))
            data=data[3:]
        load.close()
    def Draw(self):
        pygame.event.clear([KEYUP])
        self.surf.fill((0,0,0))

        if self.world.good==1:
            if self.world.keys[K_ESCAPE]:
                self.world.ChangeState("game")
                
        
        if not self.world.keys[K_ESCAPE]:
            self.world.good=1
    
        
        for e in self.world.events:
            if e.type == QUIT:
                self.world.savelvl(self.world.containing,self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt")
                self.world.go = False

        if self.created==0:
            self.CreateSmallMap(str(self.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small)
            self.created=1
        else:
            self.small.draw(self.surf)

class Button(Entity):
    def __init__(self,surf):
        pass

            
            
            
        
