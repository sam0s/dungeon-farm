#!/usr/bin/env python

"""
questmenu.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []


import pygame,json
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
        self.allQuests=loadAllQuests()
        self.goBackTo="overworld"

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
                #self.surf.fill((0,0,0))
                self.surf.blit(self.menuimg,(0,0))
                pygame.display.update()
                self.drawn=True
                padding=0
                self.qbuttons=[]
                self.qIds=[]
                for f in self.quests:
                    if f.active:
                        self.qIds.append(f.id)
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
                        self.game.state=self.goBackTo

            if e.type == MOUSEBUTTONUP and e.button == 1:
                if self.screen=="quests":
                    if len(self.qbuttons)>0:
                        for b in self.qbuttons:
                            if b.rect.collidepoint(e.pos):
                                self.screen="questDescr"
                                self.drawn=False
                                #fix this
                                targetId=self.qIds[self.qbuttons.index(b)]
                                qlist=[x for x in self.quests if x.id == targetId]
                                self.selectedQuest=qlist[0]
                                self.selectedQuest.check(self.game)

                for b in self.mainbuttons:
                    if b.rect.collidepoint(e.pos):
                        if self.screen=="quests":
                            self.drawn=False
                            self.good=False
                            self.game.ow.good=True
                            self.game.state=self.goBackTo
                        else:
                            self.drawn=False
                            self.screen="quests"
            if e.type==QUIT:
                self.game.go=False

class Quest(object):
    def __init__(self, id, name, descr, active=False, tasks=None, rewards=[]):
        self.name = name
        self.descr = descr
        self.active = active
        self.tasks = tasks if tasks else []
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
        self.location = False

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

class PlayerQuestTask(Task):
    """
    Task to see if a player has completed a certain quest. (based on ID)
    """
    def __init__(self,format,questID):
        Task.__init__(self)
        self.format=format
        self.questID=questID
    def check(self,game):
        print "Checking completed quests for ID"
        print self.questID

        for f in [x for x in game.qm.quests if not x.active]:
            self.completed=int(f.id)==self.questID

        return self.completed

    def descr(self):
        return self.format

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

class PlayerFetchTask(Task):
    """
    Task allowing to check if a certain Player has found a certain item from dungeon.
    """
    def __init__(self, format, itemID, location):
        Task.__init__(self)
        self.format = format
        self.itemID = itemID
        self.location=location

    def check(self, game):
        print "Checking player's items for item with ID"
        print self.itemID

        c=0
        for f in game.player.inventory:
            if f.id==self.itemID:
                game.player.inventory.pop(game.player.inventory.index(f))
                c+=1
        self.completed=c>0

        return self.completed

    def descr(self):
        return self.format

##########################################################################
# LOAD ALL QUESTS (while only opening the file one time lol)

def loadAllQuests():
    allQuests={}
    #try:
    with open(path.join("quests.json")) as f:
        jsondata = json.load(f)

    taskTypes = {
    'PlayerPropTask':PlayerPropTask,
    'PlayerItemTask':PlayerItemTask,
    'PlayerFetchTask':PlayerFetchTask,
    'PlayerQuestTask':PlayerQuestTask
    }

    for qId in range(999):
        qId=str(qId)

        try:
            QUEST = Quest(qId,jsondata[qId]['name'],jsondata[qId]['descr'],active=True,rewards=[jsondata[qId]['rew']])
        except KeyError:
            print "No quest with id "+qId
            qId="skip"

        if qId != "skip":
            print "te"
            for f in jsondata[qId]['tasks']:
                tp=f['type']
                if tp=="PlayerFetchTask":
                    QUEST.addTasks(PlayerFetchTask(f['format'],int(f['itemID']),f['location']))
                if tp=="PlayerItemTask":
                    QUEST.addTasks(PlayerItemTask(f['format'],f['item'],f['count']))
                if tp=="PlayerPropTask":
                    QUEST.addTasks(PlayerPropTask(f['format'],f['prop'],f['count']))
                if tp=="PlayerQuestTask":
                    QUEST.addTasks(PlayerQuestTask(f['format'],f['quest']))
                allQuests[qId]=QUEST
    #except KeyError:
        #print "number of quests loaded-"+qId
    return allQuests
