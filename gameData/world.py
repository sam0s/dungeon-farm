#################################
# sam0s #######################
#################################

import pygame
from random import choice
from pygame import *
import battle,escmenu,items
from math import sqrt
import dpylib as dl

pygame.init()
font=pygame.font.Font(None,15)

class World(object):
    def __init__(self,containing,surf,hudsurf,images):
        self.images=images

        self.containing=containing
        self.drawnlevel=pygame.Surface((800,640))
        self.containing.draw(self.drawnlevel)


        #self.drawPath = pygame.sprite.Group()

        self.turn=1
        self.pos=[0,0]
        self.player=None
        self.state="menu"
        self.surf=surf
        self.hudsurf=hudsurf
        self.hudlog=dl.Log(self,439,1,360,125,(220,220,220),hudsurf)
        self.keys=pygame.key.get_pressed()
        self.go=True
        self.levelname="default"
        self.playername=""

        self.dungeonLevelCap = 5


        #are you in a battle?
        self.battle=False


        self.logtext=[]

        #this whole deal right here might be changed later
        self.bat=battle.Battle(self.surf,self)
        self.esc=escmenu.EscMenu(self.surf,self)

        #really prob need to find a better way to do this
        self.good=1
        self.mse32=(0,0)

    def Close(self,save=True):
        if save:
            dl.savelvl(self.containing,self.levelname+"\\world"+str(self.pos[0])+str(self.pos[1])+".txt",self)
            self.go = False
        else:
            self.go = False

    def SetLevel(self,lev):
        self.levelname=lev
    def SetPlayer(self,name):
        self.playername=name
    def ChangeState(self,state):
        self.good=0
        self.state=state
        if state=="escmenu":
            self.Draw()


    def Update(self,delta):
        self.delta=delta
        #Events and Keys
        self.events=pygame.event.get()
        self.keys=pygame.key.get_pressed()
        mse=pygame.mouse.get_pos()
        if self.state == "menu":
            #menu routine
            self.hudsurf.fill((0,0,0))
            self.surf.blit(self.images[1],(0,0))
            pygame.display.flip()
            for e in self.events:
                if e.type==KEYUP:
                    if e.key==K_SPACE:
                        self.state="game"
                        self.ReDraw()
                        for f in range(20):
                            self.logtext.append(".")
                if e.type==QUIT:
                    self.Close(False)
        if self.state == "game":
            self.mse32=(((mse[0])/32)*32,((mse[1])/32)*32)
            self.Draw()
            if self.good==1:
                if self.keys[K_TAB]:
                    self.esc.drawn=0
                    self.esc.created=0
                    self.ChangeState("escmenu")

            if not self.keys[K_TAB]:
                self.good=1

            for e in self.events:
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if self.player.moving==False:
                        self.player.moveto=[self.mse32[0],self.mse32[1]]
                    #Headshot Click
                    if e.pos[0]<130:
                        if e.pos[1]>512:
                            self.esc.tab="player"
                            self.ChangeState("escmenu") #player tab
                if e.type == QUIT:
                    self.Close()

            self.player.update()
            #self.drawPath.update()
            self.mouse.update()

        if self.state == "battle":
            self.bat.Draw()

        if self.state == "levelup":
            self.lvlup.Draw()


        #draw the in game menu
        if self.state == "escmenu":
            #if the player
            if self.esc.tab=="map":
                self.player.update()
            self.esc.Draw()

        self.hudlog.update(self.hudsurf)
        self.surf.blit(self.hudsurf, (0,512))
        pygame.display.flip()

    def Draw(self,yesworld=True):
        #self.surf.fill((0,0,0))
        if yesworld:
            self.surf.blit(self.drawnlevel,(0,0))
        dl.bar(self.hudsurf,(0,210,0),(210,0,0),130,4,165,25,self.player.hp,self.player.maxhp)
        dl.bar(self.hudsurf,(75,0,130),(210,0,0),130,32,165,25,self.player.xp,self.player.nextxp)
        self.hudsurf.blit(self.images[2],(1,1))
    def ReDraw(self):
        self.drawnlevel.fill((0,0,0))
        self.containing.draw(self.drawnlevel)

    def Shift(self,d):
        dl.savelvl(self.containing,self.levelname+"\\world"+str(self.pos[0])+str(self.pos[1])+".txt")
        self.esc.created=0

        if d=='n':
            self.pos=[self.pos[0],self.pos[1]-1]
            self.player.prev[1]=self.player.changey=self.player.moveto[1]=self.player.rect.y=448

            self.logtext.append("going north")
        elif d=='e':
            self.pos=[self.pos[0]+1,self.pos[1]]
            self.player.prev[0]=self.player.changex=self.player.moveto[0]=self.player.rect.x=32

            self.logtext.append("going east")
        elif d=='s':
            self.pos=[self.pos[0],self.pos[1]+1]
            self.player.prev[1]=self.player.changey=self.player.moveto[1]=self.player.rect.y=32

            self.logtext.append("going south")
        elif d=='w':
            self.pos=[self.pos[0]-1,self.pos[1]]
            self.player.prev[0]=self.player.changex=self.player.moveto[0]=self.player.rect.x=736

            self.logtext.append("going west")

        dl.changelevel(self.containing,self.levelname,self.pos)
        self.ReDraw()
