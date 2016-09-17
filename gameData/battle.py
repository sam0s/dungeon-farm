#################################
# sam0s #######################
#################################


import pygame
from random import choice
from pygame import *
import dpylib
import ui

headshots=[pygame.image.load("images\\orcheadshot.png")]


pygame.init()
font=pygame.font.Font(None,15)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Battle(object):
    def __init__(self,surf,world):
        self.surf=surf
        self.world=world
        self.enemydisp = Surface((800,128))
        self.enemydisp.fill((0,0,0))
        self.buttons=[ui.Button(300,300,100,32,"Attack",self.surf),ui.Button(300,364,100,32,"Items",self.surf)]
        self.enemy='orc'
    def EnemyAttack(self):
        if self.enemy=='orc':
            print "enemy whacks u"
        #ughh
    def Draw(self):
        self.surf.fill((0,0,220))
        self.surf.blit(self.enemydisp,(0,0,))
        self.surf.blit(headshots[0],(672,0))
        for e in self.world.events:
            #button handling
            if e.type == MOUSEBUTTONUP:
                for b in self.buttons:
                    if b.rect.collidepoint(e.pos):
                        if b==self.buttons[0]:
                            print "yu attack!"
                            self.EnemyAttack()
                        if b==self.buttons[1]:
                            self.world.ChangeState("menu")
            if e.type == QUIT:
                dpylib.savelvl(self.world.containing,self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt")
                self.world.go = False
        for b in self.buttons:
            b.Update()
            

class Button(Entity):
    def __init__(self,surf):
        pass

            
            
            
        
