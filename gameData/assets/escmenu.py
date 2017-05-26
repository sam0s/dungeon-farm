#!/usr/bin/env python

"""
escmenu.py

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

pygame.init()
font = ui.LoadFont()


itemFrame=pygame.image.load(path.join("images","items.png")).convert()


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Square(Entity):
    def __init__(self,x,y,c):
        Entity.__init__(self)
        self.image=pygame.Surface((6,6))
        self.image.fill(c)
        self.rect=(x/6,y/6,5,5)


class EscMenu(object):
    def __init__(self,surf,world):

        self.player_stats_drawn=0

        self.surf=surf
        self.world=world
        self.small = pygame.sprite.Group()
        self.tab="map"
        self.created=0

        #BUTTONS INIT
        self.tabs=[ui.Button(650,50,100,32,"Player",self.surf),
                    ui.Button(650,100,100,32,"Items",self.surf),
                    ui.Button(650,150,100,32,"Map",self.surf),
                    ui.Button(650,200,100,32,"Go Back",self.surf),
                    ui.Button(650,300,100,32,"Leave",self.surf)]

        self.invbuttons=[ui.Button(500,430,100,32,"Drop",self.surf),
                            ui.Button(500,385,100,32,"Use",self.surf)]

        self.levelbuttons=[ui.Button(150,188,16,16,"+",self.surf),
                            ui.Button(150,220,16,16,"+",self.surf),
                            ui.Button(150,252,16,16,"+",self.surf)]


        self.invx=0
        self.invy=0

        self.drawn=0

        #self.buttons=[ui.Button(300,300,100,32,"Go Back.",self.surf)]
        #self.CreateSmallMap(str(self.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small)
    def CreateSmallMap(self,loc,lev,offset=0,offsety=0):
        #self.small.empty()
        FNF=0
        try:
            load = open(loc,"r")
        except:
            FNF=1
        if FNF==0:
            read = 0
            data = load.read()
            data=data.split(".")
            data=data[:-1]

            while len(data) > 0:
                c=(0,0,0)
                if data[0]=='"wall"':
                    c=(100,100,100)
                #if data[0]=='"gold"':
                #    c=(255,255,0)
                #if data[0]=='"enemy"':
                #    c=(255,0,0)
                lev.add(Square(int(data[1])+offset,int(data[2])+offsety,c))
                data=data[3:]
            load.close()

    def Draw(self):
        #press ESC to exit menu
        if self.world.good==1:
            if self.world.keys[K_TAB]:
                self.world.ChangeState("game")
        if not self.world.keys[K_TAB]:
                self.world.good=1
        if self.drawn==0:
            self.world.ReDraw(True)
            if self.tab=="items":

                oef=230+(self.invy*42)
                oef2=43+(self.invx*38)

                self.surf.fill((0,0,0))
                self.surf.blit(itemFrame,(0,0))
                pygame.draw.circle(self.surf,(255,0,0),(oef2,oef),5,0)
                x=30
                y=229
                for f in self.world.player.activeWeapon:
                    self.surf.blit(f.image,(30,16))
                for f in self.world.player.inventory:
                    #pygame.draw.rect(self.surf,(255,0,0),(x,y,26,26),0)
                    self.surf.blit(f.image,(x,y))
                    self.surf.blit(font.render(str(f.stack),0,(255,255,255),(0,0,0)),(x,y))
                    x+=38
                    if x>470:
                        x=30
                        y+=41

            if self.tab=="player":
                x=1
                self.surf.fill((0,0,0))

                b=[
                font.render(str(self.world.playername)+": level "+str(self.world.player.level),0,(255,255,255),(0,0,0)),
                font.render("XP: "+str(self.world.player.xp)+"/"+str(self.world.player.nextxp),0,(255,255,255),(0,0,0)),
                font.render("Skill Points: "+str(self.world.player.skillpoints),0,(0,0,0),(0,0,0)),
                font.render("",0,(0,0,0),(0,0,0)),
                font.render("",0,(0,0,0),(0,0,0)),
                font.render("Attack Damage: "+str(self.world.player.atk),0,(255,255,255),(0,0,0)),
                font.render("Move Speed: "+str(self.world.player.speed),0,(255,255,255),(0,0,0)),
                font.render("Max Health: "+str(self.world.player.maxhp),0,(255,255,255),(0,0,0))
                ]
                if self.world.player.skillpoints>0:
                    b[4]=font.render("Skill Points: "+str(self.world.player.skillpoints),0,(25,255,50),(0,0,0))
                for f in b:
                    self.surf.blit(f,(32,x*32))
                    x+=1
                self.player_stats_drawn=1
            self.drawn=1

        if self.tab=="map":
            if self.created==0:
                self.surf.fill((0,0,250))
                pygame.draw.rect(self.surf,(0,0,0),(0,0,398,250),0)
                self.small.empty()

                #top
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]-1)+str(self.world.pos[1]-1)+".txt"),self.small,0)
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1]-1)+".txt"),self.small,792)
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]+1)+str(self.world.pos[1]-1)+".txt"),self.small,1584)

                #mid
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]-1)+str(self.world.pos[1])+".txt"),self.small,0,492)
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt"),self.small,792,492)
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]+1)+str(self.world.pos[1])+".txt"),self.small,1584,492)


                #bot
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]-1)+str(self.world.pos[1]+1)+".txt"),self.small,0,984)
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1]+1)+".txt"),self.small,792,984)
                self.CreateSmallMap(str(self.world.levelname+"\\world"+str(self.world.pos[0]+1)+str(self.world.pos[1]+1)+".txt"),self.small,1584,984)

                self.created=1

                self.small.draw(self.surf)
                pygame.draw.rect(self.surf,(0,255,0),((self.world.player.rect.x+792)/6,(self.world.player.rect.y+492)/6,6,6),0)


        for e in self.world.game.events:
            if e.type == MOUSEBUTTONUP and e.button == 1:
                self.drawn=0
                mse = e.pos

                if self.tab=="player":
                    if self.world.player.skillpoints>0:
                        for b in self.levelbuttons:
                            if b.rect.collidepoint(mse):
                                self.world.player.skillpoints-=1
                                if self.levelbuttons.index(b)==0:
                                    self.world.player.atk+=1
                                if self.levelbuttons.index(b)==1:
                                    self.world.player.speed+=2
                                if self.levelbuttons.index(b)==2:
                                    self.world.player.maxhp+=8

                #Handle inventory related buttons
                if self.tab=="items":
                    for b in self.invbuttons:
                        if b.rect.collidepoint(mse):
                            self.drawn=0
                            try:item=self.world.player.inventory[(self.invx+(self.invy)*12)]
                            except IndexError:print "no item selected";item=None
                            if item:
                                if b.text=="Use":
                                    if item.itemType=="food":
                                        self.world.player.hp+=item.consumeVal
                                        if self.world.player.hp>self.world.player.maxhp:self.world.player.hp=self.world.player.maxhp
                                        if item.stack==1:
                                            self.world.player.inventory[(self.invx+(self.invy)*12)].destroy()
                                        else:
                                            item.stack-=1
                                    if item.itemType=="weapon":
                                        if item.name!=self.world.player.activeWeapon[0].name:
                                            if item.stack>1:
                                                item.stack-=1
                                                self.world.player.giveItem(self.world.player.activeWeapon[0])
                                                self.world.player.activeWeapon=[item]
                                            else:
                                                self.world.player.giveItem(self.world.player.activeWeapon[0])
                                                self.world.player.activeWeapon=[item]
                                                self.world.player.inventory[(self.invx+(self.invy)*12)].destroy()


                                if b.text=="Drop":
                                        #print "dropped item"
                                        if item.stack>1:
                                            item.stack-=1
                                        else:
                                            self.world.player.inventory[(self.invx+(self.invy)*12)].destroy()
                            self.world.Draw(False)


                    #INVENTORY DOT
                    if mse[0]<485:
                        if mse[1]>228:
                            if mse[1]>426:
                                self.invy=5
                            elif mse[1]>385:
                                self.invy=4
                            elif mse[1]>343:
                                self.invy=3
                            elif mse[1]>303:
                                self.invy=2
                            elif mse[1]>262:
                                self.invy=1
                            else:
                                self.invy=0

                        if mse[0]>21:
                            if mse[0]>442:
                                self.invx=11
                            elif mse[0]>405:
                                self.invx=10
                            elif mse[0]>366:
                                self.invx=9
                            elif mse[0]>328:
                                self.invx=8
                            elif mse[0]>290:
                                self.invx=7
                            elif mse[0]>252:
                                self.invx=6
                            elif mse[0]>213:
                                self.invx=5
                            elif mse[0]>175:
                                self.invx=4
                            elif mse[0]>136:
                                self.invx=3
                            elif mse[0]>100:
                                self.invx=2
                            elif mse[0]>61:
                                self.invx=1
                            else:
                                self.invx=0


                #Handle the general buttons
                for b in self.tabs:
                    if b.rect.collidepoint(e.pos):
                        if b.text=="Go Back":
                            if self.world.battle==False:
                                self.world.ChangeState("game")
                                self.drawn=0
                            else:
                                self.world.bat.mode="fight"
                                self.world.ChangeState("battle")
                        if not self.world.battle:
                            #self.drawn=0
                            if b.text=="Leave":
                                dl.savelvl(self.world)
                                self.world.game.state="overworld"
                                self.world.state="game"
                                #dl.savelvl(self.world.containing,self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt",self.world)

                            if b.text=="Map":
                                self.created=0
                                self.tab="map"
                            if b.text=="Player":
                                self.player_stats_drawn=0
                                self.tab="player"
                            if b.text=="Items":
                                self.tab="items"
        #DRAW BUTTONS
        for e in self.world.game.events:
            if e.type == QUIT:
                self.world.Close()

        if not self.world.battle:
            for f in self.tabs:
                f.Update()
        else:
            self.tabs[3].Update()

        if self.tab=="player":
            if self.world.player.skillpoints>0:
                for f in self.levelbuttons:
                    f.Update()
        if self.tab=="items":
            for f in self.invbuttons:
                f.Update()
