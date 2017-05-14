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
font = ui.LoadFont()

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

        self.locationtitles=[font.render("Welcome to Prospect",0,(255,255,255),(0,0,0)),
                             font.render("Welcome to Fairfield",0,(255,255,255),(0,0,0)),
                             font.render("Welcome to Norfolk",0,(255,255,255),(0,0,0)),
                             font.render("Select a dungeon",0,(255,255,255),(0,0,0)),
                            ]

        self.townbuttons=[ui.Button(510,50,220,32,"Visit the town leader",self.surf),
                    ui.Button(510,100,220,32,"Visit the tavern",self.surf),
                    ui.Button(510,150,220,32,"Visit the market",self.surf),
                    ui.Button(510,200,220,32,"View nearby dungeons",self.surf),
                    ui.Button(510,250,220,32,"Go back",self.surf)
                    ]

        self.cavebuttons=[ui.Button(300,50,220,32,"Cave 1",self.surf),
                    ui.Button(300,100,220,32,"Cave 2",self.surf),
                    ui.Button(300,150,220,32,"Cave 3",self.surf)
                    ]
    def Draw(self):
        if self.screen=="town":
            if self.drawn==False:
                self.surf.fill((0,0,0))
                for b in self.townbuttons:
                    b.Update()
                if self.town=="Prospect":
                    self.surf.blit(self.locationtitles[0],(25,25))
                if self.town=="Fairfield":
                    self.surf.blit(self.locationtitles[1],(25,25))
                if self.town=="Norfolk":
                    self.surf.blit(self.locationtitles[2],(25,25))
                self.drawn=True
        if self.screen=="cave":
            if self.drawn==False:
                self.surf.fill((0,0,0))
                self.townbuttons[4].Update()
                self.surf.blit(self.locationtitles[3],(25,25))
                for b in self.cavebuttons[0:3]:
                    b.Update()
                #if self.town=="Prospect":
                self.drawn=True

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

                #OVERWORLD
                if self.screen=="main":
                    for b in self.locationbuttons:
                        if b.rect.collidepoint(e.pos):
                            self.town=b.text
                            self.screen="town"
                            self.drawn=False

                #IN A TOWN
                if self.screen=="town":
                    for b in self.townbuttons:
                        if b.rect.collidepoint(e.pos):
                            if b.text=="Go back":
                                self.screen="main"
                                self.drawn=False
                            if b.text=="View nearby dungeons":
                                self.screen="cave"
                                self.drawn=False

                #CAVE SELECTION
                if self.screen=="cave":
                    if self.townbuttons[4].rect.collidepoint(e.pos):
                        self.screen="town"
                        self.drawn=False
                    for b in self.cavebuttons:
                        if b.rect.collidepoint(e.pos):
                            #LOAD CAVE FROM INDEX
                            dl.startdungeon(self.cavebuttons.index(b),self.game.gw)
                            self.game.state="game"
                            self.screen="main"
                            self.game.gw.ReDraw()
                            for f in range(15):
                                self.game.gw.logtext.append(".")
                            self.drawn=False
            if e.type==QUIT:
                self.game.go=False
