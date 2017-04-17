#################################
# sam0s #######################
#################################

import pygame
from random import choice
from pygame import *
import battle,escmenu,items
from math import sqrt
import world
from os import path

pygame.init()
font=pygame.font.Font(None,15)

#menuimg=pygame.image.load("images\\menu.png")
#headshots=[pygame.image.load("images\\headshot1.png")]

#################################
# FUNCTIONS #######################
#################################

#save game
def savelvl(ents,loc,world=None):
    if world:
        #save stats
        f=open(world.playername+"\\"+world.playername+".txt",'w')
        #level,xp,nextxp,hp,maxhp,atk,gold,posx,posy,worldx,worldy
        allstuff=str(world.player.level)+"."
        allstuff+=str(world.player.xp)+"."
        allstuff+=str(world.player.nextxp)+"."
        allstuff+=str(world.player.hp)+"."
        allstuff+=str(world.player.maxhp)+"."
        allstuff+=str(world.player.atk)+"."
        allstuff+=str(world.player.gold)+"."
        allstuff+=str(int(world.player.moveto[0]))+"."
        allstuff+=str(int(world.player.moveto[1]))+"."
        allstuff+=str(world.pos[0])+"."
        allstuff+=str(world.pos[1])+"."
        allstuff+=str(world.player.speed)
        f.write(str(allstuff))
        f.close()

        #save inventory
        f=open(path.join(world.playername,"inv.txt"),'w')
        itemNum=0
        for a in world.player.inventory:
            if itemNum+1!=len(world.player.inventory):
                f.write(str(world.player.inventory[itemNum].id)+"_"+str(world.player.inventory[itemNum].stack)+".")
            else:
                f.write(str(world.player.inventory[itemNum].id)+"_"+str(world.player.inventory[itemNum].stack))
            itemNum+=1
        f.close()

    save = open(loc,"w")
    for f in ents:
        save.write('"'+f.name+'"'+"."+str(f.rect.left)+"."+str(f.rect.top)+".")
    save.close()

#load game
def loadlvl(ents,loc):
    load = open(loc,"r")
    read = 0
    data = load.read()
    data=data.split(".")
    data=data[:-1]
    while len(data) > 0:
        if data[0]=='"wall"':
            w=Wall(int(data[1]),int(data[2]))
        if data[0]=='"door"':
            w=Door(int(data[1]),int(data[2]))
        if data[0]=='"gold"':
            w=Pickup(int(data[1]),int(data[2]),"gold")
        if data[0]=='"life"':
            w=Pickup(int(data[1]),int(data[2]),"life")
        if data[0]=='"enemy"':
            w=Enemy(int(data[1]),int(data[2]))
        if data[0]=='"randombox"':
            w=Pickup(int(data[1]),int(data[2]),"randombox")
        ents.add(w)
        data=data[3:]
    load.close()

#draw a bar with %
def bar(surface,color1,color2,x,y,width,height,value,maxvalue):
    xx=0
    pygame.draw.rect(surface, color2, (x,y,width,height), 0)
    for hp in range(int(max(min(value / float(maxvalue) * width, width), 0))):
        pygame.draw.rect(surface, color1, (x+xx,y,1,height), 0)
        xx+= 1
    surface.blit(font.render(str(value)+"/"+str(maxvalue),0,(0,0,0)),(x+width/2-11,y+height/2-5))

#used to load into a new level
def changelevel(ents,loc,pos):
    try:
        ents.empty()
        loadlvl(ents,loc+"\\world"+str(pos[0])+str(pos[1])+".txt")
    except:
        fill(ents)
        carve(ents)
        doors(ents)
        savelvl(ents,loc+"\\world"+str(pos[0])+str(pos[1])+".txt")

#carve out the level
def carve(ents):
    x = 32
    y = 32
    direction = choice([1,2,3,4])
    lastdir = direction
    rect = pygame.Rect(x,y,8,8)
    total = 0
    carvnum = choice([95,100,110,125,130,150,200,225])
    while total < carvnum:
        total+=1

        #generate cool stuff
        special=choice(([1]*4) #gold rate
                       +([2]*3)#enemy rate
                       +([3]*1)#random box rate
                       +([4]*2)#life drop rate
                       +([0]*104) #empty rate
                       )
        if special==1:
            ents.add(Pickup(x,y,"gold"))
        if special==2:
            ents.add(Enemy(x,y))
        if special==3:
            ents.add(Pickup(x,y,"randombox"))
        if special==4:
            ents.add(Pickup(x,y,"life"))

        while direction == lastdir:
            direction = choice([1,2,3,4])
        lastdir = direction
        if direction == 1:
            for f in range(choice([3,4,5,9,15])):
                if x<736: x+=32
                rect = pygame.Rect(x,y,2,2)
                for ff in ents:
                    if rect.colliderect(ff.rect):
                        ents.remove(ff)
        if direction == 2:
            for f in range(choice([3,4,5,9,15])):
                if x>32: x-=32
                rect = pygame.Rect(x,y,2,2)

                for ff in ents:
                    if rect.colliderect(ff.rect):
                        ents.remove(ff)
        if direction == 3:
            for f in range(choice([3,4,5,9])):
                if y<448:y+=32
                rect = pygame.Rect(x,y,16,16)

                for ff in ents:
                    if rect.colliderect(ff.rect):
                        ents.remove(ff)
        if direction == 4:
            for f in range(choice([3,4,5,9])):
                if y>32: y-=32
                rect = pygame.Rect(x,y,2,2)

                for ff in ents:
                    if rect.colliderect(ff.rect):
                        ents.remove(ff)

#fill the room with blocks, before carving it
def fill(ents):
    x=y=0
    while y < 510:
        while x < 800:
            w=Wall(x,y)
            ents.add(w)
            x+=32
        x=0
        y+=32

#create doors on each side of the room
def doors(ents):
    x=384
    y=224
    while x<900:
        x+=32
        rect = pygame.Rect(x,y,2,2)
        for ff in ents:
            if rect.colliderect(ff.rect):
                ents.remove(ff)
    while x>-200:
        x-=32
        rect = pygame.Rect(x,y,2,2)
        for ff in ents:
            if rect.colliderect(ff.rect):
                ents.remove(ff)

    x=384
    while y<900:
        y+=32
        rect = pygame.Rect(x,y,2,2)
        for ff in ents:
            if rect.colliderect(ff.rect):
                ents.remove(ff)
    while y>-900:
        y-=32
        rect = pygame.Rect(x,y,2,2)
        for ff in ents:
            if rect.colliderect(ff.rect):
                ents.remove(ff)
    ents.add(Door(768,224))
    ents.add(Door(384,480))
    ents.add(Door(384,0))
    ents.add(Door(0,224))

#varition of A* pathfinding
def findpath(s,e,world):
    #world.drawPath.empty()
    s=[s[0],s[1]]
    e=[e[0],e[1]]

    dontuse=[[s[0],s[1]]]
    movelist=[]

    current=[s[0],s[1]]

    t=Pathfinder(world.mse32[0],world.mse32[1],world,1,e)
    if len(pygame.sprite.spritecollide(t,world.containing,False))>0:
        if pygame.sprite.spritecollide(t,world.containing,False)[0].name=="wall":
            #world.drawPath.empty()
            movelist=[[s[0],s[1]]]
            return movelist
    if e[1]>620:
        movelist=[[s[0],s[1]]]
        return movelist

    #YOU ARE A*
    ds=0
    while current != e:

        ds+=1
        u=Pathfinder(current[0],current[1]-32,world,ds,e)
        d=Pathfinder(current[0],current[1]+32,world,ds,e)
        l=Pathfinder(current[0]-32,current[1],world,ds,e)
        r=Pathfinder(current[0]+32,current[1],world,ds,e)
        #world.drawPath.add(u);world.drawPath.add(d);world.drawPath.add(l);world.drawPath.add(r)
        scores=[u,d,l,r]
        scoresnum=[]

        #SIFT REAL GOOD
        if len(pygame.sprite.spritecollide(u,world.containing,False))>0:
            if pygame.sprite.spritecollide(u,world.containing,False)[0].name=="wall":scores.pop(scores.index(u));#world.drawPath.remove(u)
        if len(pygame.sprite.spritecollide(d,world.containing,False))>0:
            if pygame.sprite.spritecollide(d,world.containing,False)[0].name=="wall":scores.pop(scores.index(d));#world.drawPath.remove(d)
        if len(pygame.sprite.spritecollide(l,world.containing,False))>0:
            if pygame.sprite.spritecollide(l,world.containing,False)[0].name=="wall":scores.pop(scores.index(l));#world.drawPath.remove(l)
        if len(pygame.sprite.spritecollide(r,world.containing,False))>0:
            if pygame.sprite.spritecollide(r,world.containing,False)[0].name=="wall":scores.pop(scores.index(r));#world.drawPath.remove(r)

        if [u.rect.x,u.rect.y] in dontuse:scores.pop(scores.index(u));#world.drawPath.remove(u)
        if [d.rect.x,d.rect.y] in dontuse:scores.pop(scores.index(d));#world.drawPath.remove(d)
        if [l.rect.x,l.rect.y] in dontuse:scores.pop(scores.index(l));#world.drawPath.remove(l)
        if [r.rect.x,r.rect.y] in dontuse:scores.pop(scores.index(r));#world.drawPath.remove(r)
        print scores
        if len(scores)==0:
            #world.drawPath.empty()
            movelist=[[s[0],s[1]]]
            return movelist

        for f in scores:
            scoresnum.append(f.score)
        for f in scores:
            if f.score==min(scoresnum):
                current=[f.rect.x,f.rect.y]
                dontuse.append(current)
        movelist.append(current)
        if len(movelist)>5:
            return movelist
    return movelist

#manhattan distance calculator
def mdistance(s,e):
    ns=[s[0],s[1]]
    ne=[e[0],e[1]]
    total=0
    while ne!=ns:
        if ns[0]<ne[0]:
            ns[0]+=32
            total+=32
        if ns[0]>ne[0]:
            ns[0]-=32
            total+=32
        if ns[1]<ne[1]:
            ns[1]+=32
            total+=32
        if ns[1]>ne[1]:
            ns[1]-=32
            total+=32
    return total/32



#################################
# CLASSES #######################
#################################


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class TextHolder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#Used for pathfinding
class Pathfinder(Entity):
    def __init__(self,x,y,world,ds,e):
        Entity.__init__(self)
        self.name = "pfinder"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((255,25,25))
        self.rect = Rect(x,y,32,32)
        self.world=world

        #destination
        self.ending=e

        #distance from start
        self.ds=ds

        #distance to destination
        self.de=mdistance((self.rect.x,self.rect.y),e)

        #A* score
        self.score=self.ds+self.de

    def update(self):
        s=font.render(str(self.score),0,(255,255,255),(0,0,0))
        pygame.draw.rect(self.world.surf,(255,0,0),(self.rect.x,self.rect.y,32,32),1)
        self.world.surf.blit(s,(self.rect.x+16,self.rect.y+16))


class Pickup(Entity):
    def __init__(self,x,y,ptype):
        Entity.__init__(self)
        self.name = "pickup"
        self.ptype = ptype
        self.image = Surface((32,32))
        self.image.convert()
        if self.ptype == "gold":
            self.name="gold"
            self.image.fill((255,255,0))
        if self.ptype == "life":
            self.name="life"
            self.image.fill((0,195,0))
        if self.ptype == "food":
            self.name="food"
            self.image.fill((120,60,10))
        if self.ptype == "randombox":
            self.name="randombox"
            self.image.fill((0,50,200))
        self.rect = Rect(x,y,32,32)



class Enemy(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "enemy"
        self.etype = "grunt"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((255,0,0))
        self.rect = Rect(x,y,32,32)


class Wall(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "wall"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((100,100,100))
        self.rect = Rect(x,y,32,32)

class Door(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "door"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((139,69,19))
        self.rect = Rect(x,y,32,32)

class Mouse(Entity):
    def __init__(self,x,y,world):
        Entity.__init__(self)
        self.name = "mouse"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((255,25,25))
        self.rect = Rect(x,y,32,32)
        self.world=world
    def update(self):
        self.rect.x=self.world.mse32[0]
        self.rect.y=self.world.mse32[1]
        pygame.draw.rect(self.world.surf,(255,0,0),(self.rect.x,self.rect.y,32,32),1)

class Log(TextHolder):
    def __init__(self,world,x,y,sizex,sizey,ic,surf):
        TextHolder.__init__(self)
        self.rect=pygame.Rect(x,y,sizex,sizey)

        self.world=world
        self.drawntext=[]
        #INNER AND OUTER COLORS
        self.ic=ic
        self.oc=(0,0,0)
        self.textY=4

    def update(self,surf):

        if len(self.world.logtext)>0:
            for f in self.world.logtext:
                self.drawntext.append(self.world.logtext[0])
                self.world.logtext=self.world.logtext[1:]
                if len(self.drawntext)>10:
                    pygame.draw.rect(surf,(self.ic),self.rect,0)
                    pygame.draw.rect(surf,(self.oc),self.rect,3)
                    self.drawntext=self.drawntext[1:]

            y=4
            a=0

            for f in self.drawntext:

                wax=font.render(str(self.drawntext[a]),0,(255,0,0),self.ic)
                surf.blit(wax,(self.rect.x+5,y))
                a+=1
                y+=12
