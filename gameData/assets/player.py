#!/usr/bin/env python

"""
player.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []



import pygame
from random import choice
from pygame import *
import battle,escmenu,items
from math import sqrt
import dpylib as dl
from assets.gamelib import AnimationSet, Animator
from os import path


class Player(object):
    def __init__(self,x,y,world):
        #dl.Entity.__init__(self)
        self.world = world
        self.name = "player"
        self.image = Surface((32,32))
        self.image.convert()
        self.rect = Rect(x,y,32,32)
        self.prev = self.moveto = [x,y]
        self.pfinder = None
        self.movelist = []
        self.moving = False
        self.inventory = []
        self.activeWeapon = [items.Dirk()]

        self.changex = float(self.rect.x)
        self.changey = float(self.rect.y)

        #Stats
        self.level=1
        self.hp=100
        self.xp=0
        self.nextxp=120
        self.gold=0
        self.kills=0
        #Skills
        self.skillpoints=0
        self.atk=7
        self.speed=70
        self.maxhp=100

        self.player_anim = AnimationSet(path.join("images", "player_14.png"), (16, 24))
        self.player_anim.addAnim("walk_down", 0, 3)
        self.player_anim.addAnim("walk_right", 4, 7)
        self.player_anim.addAnim("walk_left", 8, 11)
        self.player_anim.addAnim("walk_up", 12, 15)
        self.animator = Animator(self.player_anim, Animator.MODE_LOOP, 5)
        self.animator.setAnim("walk_down")

    def reset(self):
        x=384
        y=224
        self.rect = Rect(x,y,32,32)
        self.prev = self.moveto = [x,y]
        self.movelist = []
        self.moving = False
        self.changex = float(self.rect.x)
        self.changey = float(self.rect.y)

    def setAttrs(self,level=1,xp=0,hp=100,maxhp=100,atk=7,gold=0,movespeed=70,kills=0):
        self.hp=int(hp)
        self.maxhp=int(maxhp)
        self.level=int(level)
        self.atk=int(atk)
        self.xp=int(xp)
        self.nextxp=120+int(level-1)*120
        self.gold=int(gold)
        self.speed=int(movespeed)
        self.kills=int(kills)

    def giveItem(self,item):
        if len(self.inventory)==72:
            pass
        else:
            y=0
            for f in self.inventory:
                if f.name==item.name:
                    f.stack+=1
                    y=1
            if y==0:
                self.inventory.append(item)


    def levelUp(self):
        #LEVEL UP
        self.world.logtext.append("Level Up!")
        self.level+=1
        self.skillpoints+=5

        #Restore Player Health
        self.maxhp+=15
        self.hp=self.maxhp

        #CHANGE THIS LATER
        self.nextxp=120+int(level-1)*120
        if self.xp>=self.nextxp:
            self.xp=self.xp-self.nextxp
            self.levelUp()

    def giveXp(self,xp):
        self.xp+=xp
        print self.xp
        print self.nextxp
        if self.xp>=self.nextxp:
            self.xp=self.xp-self.nextxp
            self.levelUp()

    def update(self):
        self.animator.render(self.world.surf, (self.rect.x+8,self.rect.y+4))

        if self.pfinder:
            # update/draw pathfinder process
            # pass steps and render surf to `update` to enable debugging
            self.pfinder.update()
            if self.pfinder.path:
                # pathfinder has finished!
                self.movelist = self.pfinder.path
                print "Path " + str(self.movelist)
                self.moving=True
                self.pfinder = None
        elif not self.moving:
            self.prev=[self.rect.x,self.rect.y]
            if self.moveto!=self.prev:
                #print "Not moving %s->%s" % (self.prev, self.moveto)
                self.pfinder = dl.PathFinder(self.world, self.prev, self.moveto)
        else:
            #collision
            cl=pygame.sprite.spritecollide(self, self.world.containing, False)
            if cl:
                for f in cl:
                    if f.name=='door':
                        self.movelist=[]
                        if self.rect.y<64:
                            self.world.Shift('n')
                        elif self.rect.x>704:
                            self.world.Shift('e')
                        elif self.rect.y>416:
                            self.world.Shift('s')
                        elif self.rect.x<64:
                            self.world.Shift('w')
                    if f.name=='enemy':
                        self.world.bat.NewEnemy()
                        self.world.battle=True
                        self.world.ChangeState("battle")
                        self.world.containing.remove(f)
                    if f.name=='gold':
                        self.giveXp(2*self.level+1)
                        self.world.logtext.append("You find a gold coin.")
                        self.world.containing.remove(f)
                        self.gold+=1
                    if f.name=='life':
                        self.world.containing.remove(f)
                        self.world.logtext.append("You absorb 15% life points from the orb!")
                        self.hp+=(15*self.maxhp)/100
                        if self.hp>self.maxhp:
                            self.hp=self.maxhp
                    if f.name=="randombox":
                        #Give a random item
                        item=items.randomItem()
                        self.giveItem(item)
                        self.world.logtext.append("You found "+item.name)
                        self.world.containing.remove(f)

                    self.world.ReDraw()


            #move based on time delta
            if len(self.movelist)>0:
                self.moveto=self.movelist[0]
                if self.rect.x<self.moveto[0]:
                    self.animator.setAnim("walk_right")
                    self.changex+=(self.speed)*self.world.delta
                    if self.changex>self.moveto[0]-1:self.changex=self.moveto[0]
                elif self.rect.x>self.moveto[0]:
                    self.animator.setAnim("walk_left")
                    self.changex-=(self.speed)*self.world.delta
                    if self.changex<self.moveto[0]+1:self.changex=self.moveto[0]
                elif self.rect.y<self.moveto[1]:
                    self.animator.setAnim("walk_down")
                    self.changey+=(self.speed)*self.world.delta
                    if self.changey>self.moveto[1]+1:self.changey=self.moveto[1]
                elif self.rect.y>self.moveto[1]:
                    self.animator.setAnim("walk_up")
                    self.changey-=(self.speed)*self.world.delta
                    if self.changey<self.moveto[1]-1:self.changey=self.moveto[1]
                else:
                    self.prev=self.movelist[0]
                    self.movelist.pop(0)
                    #self.world.ReDraw()
            else:
                self.moving=False

            #draw player
            self.animator.update(self.world.delta)


            self.rect.x=int(self.changex)
            self.rect.y=int(self.changey)
