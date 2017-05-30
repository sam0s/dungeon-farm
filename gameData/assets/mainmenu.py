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
                    ui.Button(650,200,100,32,"Quit",self.surf)]
    def Draw(self):
        if self.screen=="main":
            #menu routine
            if not self.drawn:
                #self.surf.fill((0,0,0))
                self.surf.blit(self.menuimg,(0,0))
                pygame.display.update()
                self.drawn=True
            for f in self.mainbuttons:
                f.Update()
            for e in self.game.events:
                if e.type == MOUSEBUTTONUP and e.button == 1:
                    for b in self.mainbuttons:
                        if b.rect.collidepoint(e.pos):
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
