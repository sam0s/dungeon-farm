#################################
# sam0s #######################
#################################


import pygame
from random import choice
from pygame import *
import dpylib
import ui

pygame.init()
font=pygame.font.Font(None,15)

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
        self.small2 = pygame.sprite.Group()
        self.tab="map"
        self.created=0
        self.tabs=[ui.Button(650,50,100,32,"Player",self.surf),ui.Button(650,100,100,32,"Items",self.surf),ui.Button(650,150,100,32,"Map",self.surf),ui.Button(650,200,100,32,"Go Back",self.surf)]

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
                if data[0]=='"gold"':
                    c=(255,255,0)
                if data[0]=='"enemy"':
                    c=(255,0,0)
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
            if self.tab=="items":
                self.surf.fill((0,0,0))
                self.surf.blit(self.world.images[0],(0,0))
                x=30
                y=229
                for f in self.world.player.inventory:
                    

                    pygame.draw.rect(self.surf,(255,0,0),(x,y,26,26),0)
                    self.surf.blit(font.render(str(f.stack),0,(255,255,255),(0,0,0)),(x,y))

                    x+=38
                    if x>470:
                        x=30
                        y+=41

            if self.tab=="player":
                x=1
                self.surf.fill((0,0,0))
                b=[font.render(str(self.world.playername)+": level "+str(self.world.player.level),0,(255,255,255),(0,0,0)),
                   font.render("XP: "+str(self.world.player.xp)+"/"+str(self.world.player.nextxp),0,(255,255,255),(0,0,0)),
                   font.render("Attack Damage: "+str(self.world.player.atk),0,(255,255,255),(0,0,0))
                   ]
                for f in b:
                    self.surf.blit(f,(32,x*32))
                    x+=1
                self.player_stats_drawn=1
            self.drawn=1

        if self.tab=="map":
            self.surf.fill((0,0,250))
            pygame.draw.rect(self.surf,(0,0,0),(0,0,398,250),0)

            if self.created==0:
                self.small.empty()


                #SEND NUDES
                
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
            else:
                self.small.draw(self.surf)
                pygame.draw.rect(self.surf,(0,255,0),((self.world.player.rect.x+792)/6,(self.world.player.rect.y+492)/6,6,6),0)
                            
        for e in self.world.events:
            #button handling
            for e in self.world.events:
                if e.type == QUIT:
                    self.world.Close()
            if e.type == MOUSEBUTTONUP:
                self.drawn=0
                for b in self.tabs:
                    if b.rect.collidepoint(e.pos):
                        self.player_stats_drawn=0
                        if b.text=="Go Back":
                            self.world.ChangeState("game")
                        if b.text=="Map":
                            self.tab="map"
                        if b.text=="Player":
                            self.player_stats_drawn=0
                            self.tab="player"
                        if b.text=="Items":
                            self.tab="items"
                        
        for f in self.tabs:
            f.Update()
        #self.surf.blit()

            
            
            
        
