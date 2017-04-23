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
import dpylib as dl
import ui
from os import path

mainmenu=pygame.image.load(path.join("images","menu.png")).convert()


class Menu(object):
    def __init__(self,surf,world):
        self.screen="main"
        self.surf=surf
        self.world=world
        self.go=True
        self.drawn=False
        self.menuimg=mainmenu
    def Draw(self):
        if self.screen=="main":
            #menu routine
            if not self.drawn:
                self.surf.fill((0,0,0))
                self.surf.blit(self.menuimg,(0,0))
                pygame.display.update()
                self.drawn=True
            for e in self.world.events:
                if e.type==KEYUP:
                    if e.key==K_SPACE:
                        self.world.state="game"
                        self.world.ReDraw()
                        for f in range(15):
                            self.world.logtext.append(".")

                if e.type==QUIT:
                    self.world.Close()
