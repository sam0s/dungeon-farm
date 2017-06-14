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
font = ui.LoadFont(17)
font2 = ui.LoadFont(19)
font3 = ui.LoadFont(38)
class Menu(object):
    def __init__(self,surf):
        self.screen="quests"
        self.surf=surf
        self.go=True
        self.drawn=False
        self.menuimg=backDrop
        self.mainbuttons=[ui.Button(650,420,100,32,"Go Back",self.surf)]
        self.qbuttons=[]
        self.good=False
        self.completedQuests=[]
    def Draw(self):
        if self.screen=="questDescr":
            if self.drawn==False:
                self.surf.blit(self.menuimg,(0,0))
                self.surf.blit(font3.render(self.selectedQuest.name,0,(0,0,0)),(40,50))

                y=90
                for f in self.selectedQuest.descr:
                    self.surf.blit(font2.render(f,0,(0,0,0)),(342,y))
                    y+=25

                y=120
                for t in self.selectedQuest.tasks:
                    descr = "[X] " if t.completed else "[ ] "
                    descr += t.descr()
                    self.surf.blit(font.render(descr,0,(0,0,0)),(42,y))
                    y+=25


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
                                self.selectedQuest.check(self.game)
                                if self.selectedQuest.active==False:
                                    self.quests.pop(self.quests.index(self.selectedQuest))
                                    self.completedQuests.append(self.selectedQuest)
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


class Quest(object):
    def __init__(self, id, name, descr, active=False, tasks=[], rewards=[]):
        self.name = name
        self.descr = descr
        self.active = active
        self.tasks = tasks
        self.rewards = rewards
        self.id = id

    def addTasks(self, *tasks):
        # Allow single or list of tasks
        self.tasks.extend(tasks)

    def addRewards(self, *rewards):
        self.rewards.extend(rewards)

    def check(self, game):
        if self.active:
            for t in self.tasks:
                t.check(game)

        # TODO: Game logic should be controlling when quests get rewarded
        # instead of doing it instantly.
        return self.reward(game)

    def completed(self):
        # Only check `completed` attribute instead of running full check.
        for t in self.tasks:
            if not t.completed:
                return False
        return True

    def reward(self, game):
        if not self.active or not self.completed():
            return False

        game.ow.logtext.append("%s quest completed!" % self.name)

        # Only handle XP rewards for now
        xp = 0
        xp += sum(self.rewards)
        game.player.giveXp(xp)
        game.ow.logtext.append("You gain %d experience points." % xp)
        self.active = False
        return True


class Task(object):
    """
    Task Baseclass
    Used this as a start to all other Tasks Types.
    """
    def __init__(self):
        self.completed = False

    def check(self, game):
        return self.completed

    def descr(self):
        return "[Empty Task]"


class PlayerPropTask(Task):
    """
    Task allowing to check if a certain Player property has reached a certain value.
    """
    def __init__(self, format, prop, count):
        Task.__init__(self)
        self.format = format
        self.prop = prop
        self.count = count

    def check(self, game):
        print "Checking player.%s(%d) > %d" % (self.prop, getattr(game.player, self.prop), self.count)
        self.completed = getattr(game.player, self.prop) >= self.count
        return self.completed

    def descr(self):
        return self.format.format(prop=self.prop, count=self.count)

class PlayerItemTask(Task):
    """
    Task allowing to check if a certain Player has found a certain item(s).
    """
    def __init__(self, format, item, count):
        Task.__init__(self)
        self.format = format
        self.item = item
        self.count = count

    def check(self, game):
        print "Checking player's items for "+self.item

        c=0
        for f in game.player.inventory:
            if f.name==self.item:
                game.player.inventory.pop(game.player.inventory.index(f))
                c+=1
        self.completed=c>=self.count

        return self.completed

    def descr(self):
        return self.format.format(item=self.item, count=self.count)


##########################################################################
# SAMPLE QUESTS

QUEST_001 = Quest(1,"New Adventurer",
                  ["As a new adventurer, the quest-giver of",
                    "Prospect has tasked you with finding ten ",
                    "gold as well as slaying 5 monsters.",
                    "",
                    "Your reward is 150 experience points."], True)
QUEST_001.addTasks(PlayerPropTask("Find {count} {prop}.", 'gold', 5),
                   PlayerPropTask("Kill {count} monsters.", 'kills', 3))
QUEST_001.addRewards(100)

QUEST_002 = Quest(2,"Find Gabe",
                 ["A man has posted about a missing friend",
                 "you are tasked with finding his lost",
                 "friend in prospects 2nd dungeon.",
                 "",
                 "Your reward is 25 gold, and also",
                 "100 expereince points."],active=True,tasks=[PlayerItemTask("Find {item}.", 'gabe', 1)],rewards=[100])


QUEST_003 = Quest(3,"The world is your oyster",
                  ["They say the worlds your oyster.",
                   "But oysters ain't for you.",
                   "Find an apple."],
                   active=True,
                   tasks=[PlayerItemTask("Find an {item}", 'apple', 1)],
                   rewards=[50]
)
