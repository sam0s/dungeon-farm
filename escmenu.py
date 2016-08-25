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
        self.image=pygame.Surface((16,16))
        self.image.fill(c)
        self.rect=(x/2,y/2,16,16)
    

class EscMenu(object):
    def __init__(self,surf,world,loc):
        self.surf=surf
        self.world=world
        self.levelname=loc
        self.small = pygame.sprite.Group()
        self.CreateSmallMap(str(self.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small)
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
            if data[0]=='"gold"':
                c=(255,255,0)
            if data[0]=='"enemy"':
                c=(255,0,0)
            if data[0]=='"chest"':
                c=(120,60,10)
            lev.add(Square(int(data[1]),int(data[2]),c))
            data=data[3:]
        load.close()
    def Draw(self):
        coolbeans=[]
        self.surf.fill((0,0,0))
        

        self.small.draw(self.surf)
            

        
        pygame.draw.rect(self.surf,(255,0,0),(0,0,100,100),0)
        key=pygame.key.get_pressed()
        if key[K_SPACE]:
            self.world.state="game"

class Button(Entity):
    def __init__(self,surf):
        pass

            
            
            
        
