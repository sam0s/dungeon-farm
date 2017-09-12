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

overworldimage = pygame.image.load(path.join("images","worldmap.png")).convert()
overworldimage=pygame.transform.scale(overworldimage,(1600,1024))

font = ui.LoadFont(30)

#MAKE OTHER TOWNS

class Overworld(object):
    def __init__(self,surf):
        self.screen = "main"
        self.surf = surf
        self.good = True
        self.hudsurf = Surface((800,128))

        #First item is townIndex, corresponding item is list of quests for that town (questBoardList)
        self.questBoardList = {0:[10,20,12],
                               1:[30,40,50],
                               2:[],
                               3:[],
                               4:[500]}
        self.qbuttons = []

        self.hudsurf.fill((3,3,3))
        self.logtext = ["."]*11
        self.hudlog = dl.Log(self,439,1,360,125,(220,220,220),self.hudsurf)
        self.go = True
        self.drawn = False
        self.game = None
        self.overworldimg = overworldimage

        #cool stuff
        self.offsetx=0
        self.offsety=0
        self.goto=[0,0]


        self.boundingRect=pygame.Rect((22,22),(500,500))

        self.locationrects=[
        pygame.Rect((50,70),(245,245)),
        pygame.Rect((692,20),(245,245)),
        pygame.Rect((215,632),(245,245)),
        pygame.Rect((700,700),(245,245)),
        pygame.Rect((1280,200),(245,245))
        ]

        self.townRef={0:'Prospect',1:"Fairfield",2:"Norfolk",3:"New Medford",4:"Easton"}

        self.locationtitles = [font.render("Welcome to Prospect",0,(255,255,255),(0,0,0)),
                             font.render("Welcome to Fairfield",0,(255,255,255),(0,0,0)),
                             font.render("Welcome to Norfolk",0,(255,255,255),(0,0,0)),
                             font.render("Welcome to New Medford",0,(255,255,255),(0,0,0)),
                             font.render("Welcome to Easton",0,(255,255,255),(0,0,0)),
                            ]

        self.townbuttons = [ui.Button(510,50,220,32,"View the quest board",self.surf),
                    ui.Button(510,100,220,32,"Visit the market",self.surf),
                    ui.Button(510,150,220,32,"View nearby dungeons",self.surf),
                    ui.Button(510,250,220,32,"Go back",self.surf)
                    ]

        self.cavebuttons = [ui.Button(300,50,220,32,"Cave 1",self.surf),
                    ui.Button(300,100,220,32,"Cave 2",self.surf),
                    ui.Button(300,150,220,32,"Cave 3",self.surf)
                    ]

    def Draw(self,dt):
        #Update Town Screen
        if self.screen == "town":
            if self.drawn == False:
                self.surf.fill((0,0,0))
                for b in self.townbuttons:
                    b.Update()
                #prospect
                self.surf.blit(self.locationtitles[self.townIndex],(25,25))
                self.drawn = True
        #Cave selector for towns
        if self.screen == "cave":
            if self.drawn == False:
                self.surf.fill((0,0,0))
                self.townbuttons[3].Update()
                self.surf.blit(font.render("Select a dungeon",0,(255,255,255),(0,0,0)),(25,25))
                for b in self.cavebuttons[0:3]:
                    b.Update()
                self.drawn = True
        #Show quests for the town
        if self.screen=="questboard":
            if self.drawn == False:
                self.surf.fill((0,0,0))
                self.surf.blit(font.render("Select a quest!",0,(255,255,255),(0,0,0)),(25,25))
                self.qbuttons = []
                padding = 0
                for f in self.questBoardList[self.townIndex]:
                    try:
                        f = self.game.qm.allQuests[str(f)]
                        xx = 0
                        for ff in self.game.qm.quests:
                            if f.name == ff.name:xx =- 400
                        self.qbuttons.append(ui.Button(100+xx,60+padding,200,32,f.name,self.surf))
                        padding += 42
                    except KeyError:
                        print "no quest"

                for f in self.qbuttons:
                    f.Update()

                self.townbuttons[3].Update()
                self.drawn=True

        #OVERWORLD SCREEN - NEW, IMPROVED, INTERACTIVE
        if self.screen == "main":
            dt=dt*62
            if self.goto[0] > 0:self.offsetx+=1*dt;self.goto[0]-=1*dt;
            if self.goto[0] < 0:self.offsetx-=1*dt;self.goto[0]+=1*dt;
            if self.goto[1] > 0:self.offsety+=1*dt;self.goto[1]-=1*dt;
            if self.goto[1] < 0:self.offsety-=1*dt;self.goto[1]+=1*dt;

            self.surf.fill((0,0,0))
            self.surf.blit(self.overworldimg,(self.offsetx,self.offsety))
            pygame.draw.circle(self.surf,(0,0,0),(400,320),5,0)

            for f in self.locationrects:
                if pygame.Rect(f.left+self.offsetx,f.top+self.offsety,f.width,f.height).collidepoint(400,320):
                    text="Press F to visit "+self.townRef[self.locationrects.index(f)]
                    text=font.render(text,0,(255,0,0),(0,0,0))
                    center=text.get_width()/2
                    self.surf.blit(text,(400-center,450))
                f=pygame.Rect(f.left+self.offsetx,f.top+self.offsety,f.width,f.height)
                pygame.draw.rect(self.surf,(2,2,2),f,2)
            pygame.draw.line(self.surf,(0,0,0),(400,320),(400-self.goto[0],320-self.goto[1]),3)

        #draw hud
        self.hudlog.update(self.hudsurf)
        self.surf.blit(self.hudsurf,(0,512))

        for e in self.game.events:
            if e.type == KEYUP:
                if e.key==K_ESCAPE:
                    self.game.state="menu"
                self.good = True
            if e.type == KEYDOWN:
                if e.key == K_q:
                    if self.good:
                        self.good = False
                        self.drawn = False
                        self.game.qm.goBackTo="overworld"
                        self.game.state = "quests"
                if e.key == K_f:
                    for f in self.locationrects:
                        if pygame.Rect(f.left+self.offsetx,f.top+self.offsety,f.width,f.height).collidepoint(400,320):

                            self.town = self.townRef[self.locationrects.index(f)]
                            self.townIndex = self.locationrects.index(f)
                            self.screen="town"
                            self.drawn=False
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                #OVERWORLD
                if self.screen == "main":
                    if pygame.Rect(self.boundingRect.left+self.offsetx,self.boundingRect.top+self.offsety,self.boundingRect.width,self.boundingRect.height).collidepoint(e.pos[0],e.pos[1]):
                        self.goto=[400-e.pos[0],320-e.pos[1]]

            if e.type == MOUSEBUTTONUP and e.button == 1:
                #IN A TOWN
                if self.screen == "town":
                    for b in self.townbuttons:
                        if b.rect.collidepoint(e.pos):
                            if b.text == "Go back":
                                self.screen = "main"
                                self.drawn = False
                            if b.text == "View nearby dungeons":
                                self.screen = "cave"
                                self.drawn = False
                            if b.text == "View the quest board":
                                self.screen = "questboard"
                                self.drawn = False

                #CAVE SELECTION
                if self.screen == "cave" or self.screen == "questboard":
                    if self.townbuttons[3].rect.collidepoint(e.pos):
                        self.screen="town"
                        self.drawn=False
                    if self.screen == "cave":
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
                    else:
                        for b in self.qbuttons:
                            if b.rect.collidepoint(e.pos):
                                #a=(get current town and ask the questBoardList for it's corresponding list of quets)
                                #[self.qbuttons.index(b)] tells which index to choose from the list.. it works
                                #the next line just gives the quets to the player (questMenu's list of quest)
                                a = self.questBoardList[self.townIndex][self.qbuttons.index(b)]
                                self.game.qm.quests += [self.game.qm.allQuests[str(a)]]
                                self.drawn = False

            if e.type == QUIT:
                self.game.go = False
