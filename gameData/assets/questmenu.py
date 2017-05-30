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

class Menu(object):
    def __init__(self,surf):
        self.screen="quests"
        self.surf=surf
        self.go=True
        self.drawn=False
        self.game=None
        self.menuimg=backDrop
        self.mainbuttons=[ui.Button(650,420,100,32,"Go Back",self.surf)]
        self.quests=[Quest001(self.game),Quest002(self.game)]
        self.qbuttons=[]
        self.good=False
    def Draw(self):
        if self.screen=="questDescr":
            if self.drawn==False:
                self.surf.blit(self.menuimg,(0,0))
                self.surf.blit(font.render(self.selectedQuest.descr,0,(0,0,0)),(80,80))

            pass
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
                    self.qbuttons.append(ui.Button(100,60+padding,200,32,f.name,self.surf))
                    padding+=42
                for f in self.qbuttons:
                    f.Update()
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
        self.name="First quest!"
        self.descr="Kill a single monster!"
        self.reward=100
        self.done=False
        self.req=["Kill 1 monster. [ ]"]
    def check(self):
        if self.game.player.kills>1 and self.done == False:
            self.done=True
            self.game.player.giveXp(self.reward)

class Quest002(object):
    def __init__(self,game):
        self.game=game
        self.name="Second quest!"
        self.descr="Find a sword!"
        self.reward=150
        self.done=False
        self.req=["Find a sword. [ ]"]
    def check(self):
        if self.game.player.kills>1 and self.done == False:
            self.done=True
            self.game.player.giveXp(self.reward)
