#!/usr/bin/env python

"""
world.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []



import pygame,json
from random import choice
from pygame import *
import assets.mainmenu as mainmenu
import assets.overworld as overworld
import assets.player as player
import assets.world as world
import assets.questmenu as questmenu
from math import sqrt
import dpylib as dl
from os import path

pygame.init()

class Game(object):
    def __init__(self,surf):
        self.state="menu"
        self.surf=surf

        #mainmenu objects
        self.mm=mainmenu.Menu(self.surf)
        self.mm.game=self

        #gameworld and player objects
        self.gw=world.World(self.surf)
        self.player=player.Player(384.0,224.0,self.gw)
        self.gw.game=self
        self.gw.player=self.player
        self.gw.playername="playername"

        #overworld objects
        self.ow=overworld.Overworld(self.surf)
        self.ow.game=self
        self.go=True

        #questhandler and questmenu
        self.qm=questmenu.Menu(self.surf)
        self.qm.game=self


        with open(path.join("quests.json")) as f:
            jsondata = json.load(f)


        taskTypes = {'PlayerPropTask': questmenu.PlayerPropTask}

        QUEST_0f1 = questmenu.Quest(2,jsondata['quest']['name'],jsondata['quest']['descr'],active=True,rewards=[jsondata['quest']['rew']])

        for f in jsondata['quest']['tasks']:
            print f
            QUEST_0f1.addTasks(
            taskTypes[f['type']](f['format'],f['prop'],f['count'])
            )
        self.qm.quests=[QUEST_0f1]

    def Update(self,dt):
        self.events=pygame.event.get()
        if self.state == "menu":
            self.mm.Draw()
        if self.state == "quests":
            self.qm.Draw()
        if self.state == "overworld":
            self.ow.Draw()
        if self.state == "game":
            self.gw.Update(dt)
            self.surf.blit(self.gw.surf,(0,0))
        pygame.display.flip()
