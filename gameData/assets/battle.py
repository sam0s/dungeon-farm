#!/usr/bin/env python

"""
battle.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []




import pygame
from random import choice,randint
from pygame import *
import dpylib
import ui
import enemies


pygame.init()
font = ui.LoadFont()


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
        self.mode = 'fight'

    def NewEnemy(self):
        #set level of enemy
        #Use the dungeon level cap to create the enemies level
        elvl=randint(self.world.dungeonLevelCap-4,self.world.dungeonLevelCap+1)
        self.enemy=choice([enemies.Orc(elvl),enemies.Goblin(elvl)])
        self.world.logtext.append("The "+self.enemy.name+" is level "+str(elvl)+".")

    def Attack(self):

        #player attack
        #print self.world.player.activeWeapon[0].ad
        dmg=randint(0,self.world.player.atk+self.world.player.activeWeapon[0].ad)
        self.enemy.hp-=dmg
        self.world.logtext.append(self.world.playername+" does "+str(dmg)+" damage.")
        #check for enemy death, and xp algorithim
        if self.enemy.hp<=0:
            xpgive=18*(self.enemy.level/2)+(self.enemy.level-self.world.player.level)*2
            self.world.logtext.append("Enemy Slain! "+"You get "+str(xpgive))
            self.world.player.giveXp(xpgive)
            self.world.battle=False
            self.world.ChangeState("game")
            self.world.ReDraw()


        #ENEMY ATTACK
        if self.enemy.hp>0:
            dmg=self.enemy.Attack()
            self.world.player.hp-=dmg
            self.world.logtext.append("The "+self.enemy.name+" does "+str(dmg)+" damage.")


        #test player death
        if self.world.player.hp<=0:
            self.world.game.ChangeState("menu")




    def Draw(self):
        if self.mode == 'fight':
            self.surf.fill((0,0,220))
            self.surf.blit(self.enemydisp,(0,0))
            self.surf.blit(self.enemy.image,(672,0))


            dpylib.bar(self.enemydisp,(0,210,0),(210,0,0),130,4,165,25,self.enemy.hp,self.enemy.maxhp)
            self.world.ReDraw(True)
            #dpylib.bar(self.world.hudsurf,(0,210,0),(210,0,0),130,4,165,25,self.world.player.hp,self.world.player.maxhp)
            #self.world.hudsurf.blit(self.world.images[2],(1,1))

            for e in self.world.game.events:
                #button handling
                if e.type == MOUSEBUTTONUP:
                    for b in self.buttons:
                        if b.rect.collidepoint(e.pos):
                            if b==self.buttons[0]:
                                self.Attack()
                            if b==self.buttons[1]:
                                self.mode = 'items'

                if e.type == QUIT:
                    self.world.Close()
            for b in self.buttons:
                b.Update()
        #items mode
        else:
            self.world.esc.tab="items"
            self.world.ChangeState("escmenu")


class Button(Entity):
    def __init__(self,surf):
        pass
