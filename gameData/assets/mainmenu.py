#!/usr/bin/env python

"""
mainmeu.py

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

mainmenu=pygame.image.load(path.join("images","menu.png")).convert()
optionsimg=pygame.image.load(path.join("images","menu.png")).convert()
logo_samiscool=pygame.image.load(path.join("images","samiscool_splash.png")).convert()

class Logos(object):
    def __init__(self,surf):
        self.surf=surf
        self.time=4
        self.time2=0
        self.black = pygame.Surface((800,640))
        self.black.fill((0,0,0))
        self.done=False
    def Draw(self,dt):
        if self.time>=0:
            logo_samiscool.set_alpha(12)
            self.surf.blit(logo_samiscool,(0,0))
            self.time-=1*dt
        else:
            self.time2+=1*dt
            self.black.set_alpha(3)
            self.surf.blit(self.black,(0,0))
        if self.time2>2:
            self.done=True
            self.game.state="menu"
        for e in self.game.events:
            if e.type==QUIT:
                self.game.go=False

class Menu(object):
    def __init__(self,surf):
        self.screen="main"
        self.surf=surf
        self.go=True
        self.drawn=False
        self.game=None
        self.menuimg=mainmenu
        self.mainbuttons=[ui.Button(650,50,100,32,"Continue",self.surf),
                    ui.Button(650,100,100,32,"New",self.surf),
                    ui.Button(650,150,100,32,"Options",self.surf),
                    ui.Button(650,200,100,32,"Quit",self.surf)
                    ]
        self.options=[ui.Button(650,250,100,32,"Go Back",self.surf)]

    def Draw(self):
        if self.screen=="options":
            #options routine
            if not self.drawn:
                self.surf.blit(optionsimg,(0,0))

                [x.Update() for x in self.options]
                self.drawn=True

        if self.screen=="main":
            #menu routine
            if not self.drawn:
                #self.surf.fill((0,0,0))
                self.surf.blit(self.menuimg,(0,0))
                pygame.display.update()
                [x.Update() for x in self.mainbuttons]
                self.drawn=True


        for e in self.game.events:
            if e.type == MOUSEBUTTONUP and e.button == 1:
                if self.screen == "options":
                    for b in self.options:
                        if b.rect.collidepoint(e.pos):
                            if b.text == "Go Back":
                                self.screen = "main"
                                self.drawn = False
                if self.screen == "main":
                    for b in self.mainbuttons:
                        if b.rect.collidepoint(e.pos):
                            self.game.snd.Play("button")
                            if b.text == "Options":
                                print "ef"
                                self.screen = "options"
                                self.drawn=False
                            if b.text == "Quit":
                                self.game.go=False
                            if b.text == "Continue":
                                dl.LoadGame(self.game.gw)
                                self.game.state="overworld"
                            if b.text == "New":
                                dl.NewGame(self.game.gw)
                                self.game.state="overworld"
                if e.type==QUIT:
                    self.game.go=False
