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

overworldimage=pygame.image.load(path.join("images","worldmap.png")).convert()


class Overworld(object):
    def __init__(self,surf):
        self.screen="main"
        self.surf=surf
        self.go=True
        self.drawn=False
        self.game=None
        self.overworldimg=overworldimage
        self.locationbuttons=[ui.Button(147,96,100,32,"Prospect",self.surf),
                    ui.Button(170,410,100,32,"Fairfield",self.surf),
                    ui.Button(459,37,100,32,"Norfolk",self.surf)]
    def Draw(self):
        if self.screen=="main":
            #menu routine
            if not self.drawn:
                #self.surf.fill((0,0,0))
                self.surf.blit(self.overworldimg,(0,0))
                pygame.display.update()
                self.drawn=True
            for b in self.locationbuttons:
                b.Update()
            for e in pygame.event.get():
                if e.type == MOUSEBUTTONUP and e.button == 1:
                    print "mouse"

                if e.type==QUIT:
                    self.game.go=False
