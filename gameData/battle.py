#################################
# sam0s #######################
#################################


import pygame
from random import choice,randint
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
        # [ orc , elf ,
        self.baseDamageMatrix=[6,8]
    def NewEnemy(self):
        self.enemy='orc'
        self.enemylvl=self.world.player.level+choice([1,2,3,-1,-2,-3])
        self.enemyhp=100
        print self.enemylvl
    def Attack(self):
        if self.enemy=='orc':
            dmg=self.baseDamageMatrix[0]
            dmg=randint(dmg-5,dmg)
            self.world.player.hp-=dmg
            self.world.logtext.append("The orc does "+str(dmg)+" damage.")
        if self.world.player.hp<=0:
            self.world.ChangeState("menu")
        dmg=randint(self.world.player.atk-5,self.world.player.atk)
        self.enemyhp-=dmg
        self.world.logtext.append(self.world.playerName+" does "+str(dmg)+" damage.")
        if self.enemyhp<=0:
            self.world.logtext.append("Enemy Slain!")
            self.world.logtext.append("Health Restored (alpha only)")
            self.world.player.hp=100
            self.world.ChangeState("game")
            

    def Draw(self):
        self.surf.fill((0,0,220))
        self.surf.blit(self.enemydisp,(0,0,))
        self.surf.blit(headshots[0],(672,0))


        dpylib.bar(self.enemydisp,(0,210,0),(210,0,0),130,4,165,25,self.enemyhp,self.world.player.maxhp)
        dpylib.bar(self.world.hudsurf,(0,210,0),(210,0,0),130,4,165,25,self.world.player.hp,self.world.player.maxhp)
        self.world.hudsurf.blit(dpylib.headshots[0],(1,1))

        for e in self.world.events:
            #button handling
            if e.type == MOUSEBUTTONUP:
                for b in self.buttons:
                    if b.rect.collidepoint(e.pos):
                        if b==self.buttons[0]:
                            self.Attack()
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

            
            
            
        
