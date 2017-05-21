#!/usr/bin/env python

"""
world.py

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
from os import path
import time

bagSprite=pygame.image.load(path.join("images","bag.png")).convert()
floorImage=pygame.image.load(path.join("images","floor.png")).convert()

floor=pygame.Surface((800,512))
fx=0
fy=0
while fy<512:
    while fx<800:
        floor.blit(floorImage,(fx,fy))
        fx+=32
    fx=0
    fy+=32

floorImage=floor.convert()

class World(object):
    def __init__(self,surf):
        #Create surfaces (objects & walls, drawing platflorm, new+old for transition)
        self.containing=pygame.sprite.Group()
        self.drawnlevel=pygame.Surface((800,640))
        self.new=pygame.Surface((800,512))
        self.old=pygame.Surface((800,512))

        #draw the level
        self.containing.draw(self.drawnlevel)

        #transition progress and direction(animation variable)
        self.tprog=0
        self.tdir='n'

        #self.drawPath = pygame.sprite.Group()

        self.pos=[0,0]
        self.player=None
        self.state="game"
        self.game=None
        self.surf=surf
        self.hudsurf=Surface((800,128))
        self.hudlog=dl.Log(self,439,1,360,125,(220,220,220),self.hudsurf)
        self.keys=pygame.key.get_pressed()
        self.go=True
        self.levelname="d0"
        self.playername=None
        self.mouse=dl.Mouse(0,0,self)
        self.dungeonLevelCap = 5


        #are you in a battle?
        self.battle=False


        self.logtext=[]

        #this whole deal right here might be changed later
        self.bat=battle.Battle(self.surf,self)
        self.esc=escmenu.EscMenu(self.surf,self)

        #really prob need to find a better way to do this
        self.good=1
        self.mse32=(0,0)

        self.trans=False

    def Close(self,save=True):
        dl.savelvl(self)
        self.game.go=False
    def SetPlayer(self,name):
        self.playername=name
    def ChangeState(self,state):
        self.good=0
        self.state=state
        if state=="escmenu":
            self.Draw()


    def Update(self,delta):
        self.delta=delta
        if not self.trans:
            #Events and Keys
            self.keys=pygame.key.get_pressed()
            mse=pygame.mouse.get_pos()

            if self.state == "game":
                self.mse32=(((mse[0])/32)*32,((mse[1])/32)*32)
                self.Draw()
                if self.good==1:
                    if self.keys[K_TAB]:
                        self.esc.drawn=0
                        self.esc.created=0
                        self.ChangeState("escmenu")

                if not self.keys[K_TAB]:
                    self.good=1

                for e in self.game.events:
                    if e.type == MOUSEBUTTONDOWN and e.button == 1:
                        if self.player.moving==False:
                            self.player.moveto=[self.mse32[0],self.mse32[1]]
                        #Headshot Click
                        if e.pos[0]<130:
                            if e.pos[1]>512:
                                self.esc.tab="player"
                                self.ChangeState("escmenu") #player tab
                    if e.type == QUIT:
                        self.Close()

                self.player.update()
                #self.drawPath.update()
                self.mouse.update()

            if self.state == "battle":
                self.bat.Draw()


            #draw the in game menu
            if self.state == "escmenu":
                #if the player
                if self.esc.tab=="map":
                    self.player.update()
                self.esc.Draw()

            self.hudlog.update(self.hudsurf)
            self.surf.blit(self.hudsurf, (0,512))
        else:
            #progress
            self.tprog+=300*self.delta

            #NORTH/SOUTH
            if self.tdir=='n' or self.tdir=='s':

                if self.tdir=='n':
                    self.surf.blit(self.new,(0,-512+self.tprog))
                else:
                    self.surf.blit(self.new,(0,512-self.tprog))

                if self.tdir=='n':
                    self.surf.blit(self.old,(0,self.tprog))
                else:
                    self.surf.blit(self.old,(0,-self.tprog))

                if self.tprog>512:
                    self.trans=False
                    self.tprog=0

            #EAST/WEST
            if self.tdir=='e' or self.tdir=='w':

                if self.tdir=='e':
                    self.surf.blit(self.new,(800-self.tprog,0))
                else:
                    self.surf.blit(self.new,(-800+self.tprog,0))

                if self.tdir=='e':
                    self.surf.blit(self.old,(-self.tprog,0))
                else:
                    self.surf.blit(self.old,(self.tprog,0))

                if self.tprog>800:
                    self.trans=False
                    self.tprog=0

            self.surf.blit(self.hudsurf, (0,512))

    def Draw(self,yesworld=True):
        if yesworld:
            self.surf.blit(self.drawnlevel,(0,0))

    def ReDraw(self,hudonly=False):
        if not hudonly:
            self.drawnlevel.blit(floorImage,(0,0))
            #self.drawnlevel.fill((0,32,0))
            self.containing.draw(self.drawnlevel)
        dl.bar(self.hudsurf,(0,210,0),(210,0,0),32,4,375,25,self.player.hp,self.player.maxhp)
        dl.bar(self.hudsurf,(75,0,130),(210,0,0),32,32,375,25,self.player.xp,self.player.nextxp)
    def Shift(self,d):

        #self.old.fill((0,0,0))
        #self.new.fill((0,0,0))
        self.old.blit(floorImage,(0,0))
        self.new.blit(floorImage,(0,0))
        self.containing.draw(self.old)

        #self.esc.created=0
        dl.savelvl(self)
        if d=='n':
            self.pos=[self.pos[0],self.pos[1]-1]
            self.player.prev[1]=self.player.changey=self.player.moveto[1]=self.player.rect.y=448

            self.logtext.append("going north")
        elif d=='e':
            self.pos=[self.pos[0]+1,self.pos[1]]
            self.player.prev[0]=self.player.changex=self.player.moveto[0]=self.player.rect.x=32

            self.logtext.append("going east")
        elif d=='s':
            self.pos=[self.pos[0],self.pos[1]+1]
            self.player.prev[1]=self.player.changey=self.player.moveto[1]=self.player.rect.y=32

            self.logtext.append("going south")
        elif d=='w':
            self.pos=[self.pos[0]-1,self.pos[1]]
            self.player.prev[0]=self.player.changex=self.player.moveto[0]=self.player.rect.x=736

            self.logtext.append("going west")

        dl.changelevel(self)

        #Show the shift
        self.tdir=d
        self.containing.draw(self.new)
        self.trans=True
        #self.ReDraw()
