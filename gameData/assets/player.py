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
        self.prev = [x,y]
        self.pfinder = None
        self.movelist = []
        self.moving = False
        self.inventory = []
        self.activeWeapon = [items.getItem("Dirk")]

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
        self.prev = [x,y]
        self.movelist = []
        self.moving = False
        self.changex = float(self.rect.x)
        self.changey = float(self.rect.y)

    def loadPlayer(self,data):
        #load attribute
        for atr in data['player']:
            self.hp=int(atr['hp'])
            self.maxhp=int(atr['maxhp'])
            self.level=int(atr['level'])
            self.atk=int(atr['atk'])
            self.xp=int(atr['xp'])
            self.nextxp=120+int(self.level-1)*120
            self.gold=int(atr['gold'])
            self.speed=int(atr['speed'])
            self.kills=int(atr['kills'])
            pq=atr['quests']
            n2=atr['inventory']
        #load inventory
        if n2[0]!=[]:
            for f in n2:
                #divide up by name and stack
                f2=f.split("_")
                if f2[1]=='a':
                    self.activeWeapon=[items.fromId(f2[0],self)]
                    print "Active Weapon: %s" % str(self.activeWeapon)
                    break
                #give the item
                for f3 in range(int(f2[1])):
                    it=items.fromId(f2[0],self)
                    self.giveItem(it)
        #load quests

        for q in pq:
            q=q.split("_")
            nq=self.world.game.qm.allQuests[str(q[0])]
            nq.active=q[1]=="True"
            self.world.game.qm.quests += [nq]


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
        self.world.logtext.append("5 Skill-Points added! (go to player tab)")
        self.level+=1
        self.skillpoints+=5

        #Restore Player Health
        self.maxhp+=15
        self.hp=self.maxhp

        #CHANGE THIS LATER
        self.nextxp=120+int(self.level-1)*120

    def giveXp(self,xp):
        self.xp+=xp
        while self.xp>=self.nextxp:
            self.xp-=self.nextxp
            self.levelUp()

    def moveto(self, pos):
        if self.prev == pos:
            return
        self.pfinder = dl.PathFinder(self.world, self.prev, pos)
        self.moving = False

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
        else:
            #collision
            cl=pygame.sprite.spritecollide(self, self.world.containing, False)
            if cl:
                for f in cl:
                    if f.name == 'qitem':
                        self.giveItem(f.item)
                        self.world.logtext.append("You find a quest item (%s)!" % (f.item.name))
                        self.world.containing.remove(f)
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
                moveto=self.movelist[0]
                if self.rect.x<moveto[0]:
                    self.animator.setAnim("walk_right")
                    self.changex+=(self.speed)*self.world.delta
                    if self.changex>moveto[0]-1:self.changex=moveto[0]
                elif self.rect.x>moveto[0]:
                    self.animator.setAnim("walk_left")
                    self.changex-=(self.speed)*self.world.delta
                    if self.changex<moveto[0]+1:self.changex=moveto[0]
                elif self.rect.y<moveto[1]:
                    self.animator.setAnim("walk_down")
                    self.changey+=(self.speed)*self.world.delta
                    if self.changey>moveto[1]+1:self.changey=moveto[1]
                elif self.rect.y>moveto[1]:
                    self.animator.setAnim("walk_up")
                    self.changey-=(self.speed)*self.world.delta
                    if self.changey<moveto[1]-1:self.changey=moveto[1]
                else:
                    self.prev=self.movelist.pop(0)
                    #self.world.ReDraw()
            else:
                self.moving=False

            # Update animation
            if self.moving:
                self.animator.update(self.world.delta)

            self.rect.x=int(self.changex)
            self.rect.y=int(self.changey)
