#!/usr/bin/env python

"""
questmenu.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []


import pygame
from random import choice
from pygame import *
import ui
from os import path,mkdir
from shutil import rmtree
import dpylib as dl

backDrop=pygame.image.load(path.join("images","paper.png")).convert()
font = ui.LoadFont()
font2 = ui.LoadFont(20)
class Menu(object):
    def __init__(self,surf):
        self.screen="quests"
        self.surf=surf
        self.go=True
        self.drawn=False
        self.menuimg=backDrop
        self.mainbuttons=[ui.Button(650,420,100,32,"Go Back",self.surf),ui.Button(650,90,100,32,"Check",self.surf)]
        self.qbuttons=[]
        self.good=False
    def Draw(self):
        if self.screen=="questDescr":
            if self.drawn==False:
                self.surf.blit(self.menuimg,(0,0))
                self.surf.blit(font2.render(self.selectedQuest.descr,0,(0,0,0)),(80,80))
                x=0
                y=120
                for f in self.selectedQuest.req:
                    self.surf.blit(font.render(self.selectedQuest.req[x],0,(0,0,0)),(80,y))
                    y+=25
                    x+=1



        if self.screen=="quests":
            #menu routine
            if not self.drawn:
                self.qbuttons=[]
                #self.surf.fill((0,0,0))
                self.surf.blit(self.menuimg,(0,0))
                pygame.display.update()
                self.drawn=True
                padding=0
                for f in self.quests:
                    if f.done==False:
                        self.qbuttons.append(ui.Button(100,60+padding,200,32,f.name,self.surf))
                        padding+=42
                for f in self.qbuttons:
                    f.Update()
        self.game.ow.hudlog.update(self.game.ow.hudsurf)
        self.surf.blit(self.game.ow.hudsurf,(0,512))
        for f in self.mainbuttons:
            f.Update()
        for e in self.game.events:
            if e.type==KEYUP:
                self.good=True
            if e.type==KEYDOWN:
                if e.key==K_q:
                    if self.good:
                        self.good=False
                        self.drawn=False
                        self.game.state="overworld"
            if e.type == MOUSEBUTTONUP and e.button == 1:
                if self.screen=="quests":
                    if len(self.qbuttons)>0:
                        for b in self.qbuttons:
                            if b.rect.collidepoint(e.pos):
                                self.screen="questDescr"
                                self.drawn=False
                                self.selectedQuest=self.quests[self.qbuttons.index(b)]
                for b in self.mainbuttons:
                    if b.rect.collidepoint(e.pos):
                        if b.text=="Check":
                            self.drawn=False
                            for f in self.quests:
                                f.check()
                        else:
                            if self.screen=="quests":
                                self.drawn=False
                                self.good=False
                                self.game.ow.good=True
                                self.game.state="overworld"
                            else:
                                self.drawn=False
                                self.screen="quests"
            if e.type==QUIT:
                self.game.go=False

#QUESTS
class Quest001(object):
    def __init__(self,game):
        self.game=game
        self.name="Monster Hunter"
        self.descr="Kill 3 monsters!"
        self.reward=100
        self.done=False
        self.req=["Kill 3 monsters. [ ]"]

        self.stages=1
        self.stage=[0]

    def check(self):
        print self.game.player.kills
        if self.game.player.kills>2 and self.done == False:
            self.done=True
            self.game.player.giveXp(self.reward)

class Quest002(object):
    def __init__(self,game):
        self.game=game
        self.name="Explorer"
        self.descr="Explore, and do stuff!"
        self.reward=150
        self.done=False
        self.req=["Find 10 gold. [ ]","Kill 5 monsters. [ ]"]
        self.stages=2
        self.stage=[0,0]
    def check(self):
        print self.game.player.gold
        if self.game.player.gold>9 & self.stage[0]==0:
            self.req[0]="Find 10 gold. [X]"
            self.stage[0]=1
        if self.game.player.kills>4 & self.stage[1]==0:
            self.req[1]="Kill 5 monsters. [X]"
            self.stage[1]=1
        if self.stage[0]==1 & self.stage[1]==1:
            self.game.ow.logtext.append("Second Quest completed! You gain 100 experience points.")
            self.done=True
            self.game.player.giveXp(self.reward)
