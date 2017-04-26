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
import assets.mainmenu as mainmenu
import assets.world as world
from math import sqrt
import dpylib as dl
from os import path

pygame.init()
font=pygame.font.Font(None,15)

class Game(object):
    def __init__(self,surf):
        self.state="menu"
        self.surf=surf

        #mainmenu object
        self.mm=mainmenu.Menu(self.surf)
        self.mm.game=self

        #gameworld object
        self.gw=world.World(self.surf)
        self.gw.game=self

        self.go=True
    def Update(self,dt):
        if self.state == "menu":
            self.mm.Draw()
        if self.state == "overworld":
            pass
        if self.state == "game":
            self.gw.Update(dt)
            self.surf.blit(self.gw.surf,(0,0))
        pygame.display.flip()
