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

class EscMenu(object):
    def __init__(self,surf,world,loc):
        self.surf=surf
        self.world=world
        self.levelname=loc
    def Draw(self):
        self.surf.fill((0,0,0))
        print str(self.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt")
        pygame.draw.rect(self.surf,(255,0,0),(0,0,100,100),0)
        key=pygame.key.get_pressed()
        if key[K_SPACE]:
            self.world.state="game"

class Button(Entity):
    def __init__(self,surf):
        pass

            
            
            
        
