#!/usr/bin/env python

"""
dpylib.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []



import pygame
from random import choice
from pygame import *
from math import sqrt
import player,items
from shutil import rmtree
from time import sleep
from os import path,mkdir
from ui import LoadFont

from Queue import PriorityQueue

pygame.init()
font = LoadFont()

wallImage=pygame.image.load(path.join("images","wall.png")).convert()

goldImage=pygame.image.load(path.join("images","gold.png")).convert()
goldImage.set_colorkey((0,255,0))

chestImage=pygame.image.load(path.join("images","chest.png")).convert()
chestImage.set_colorkey((0,255,0))

orbHealImage=pygame.image.load(path.join("images","orb.png")).convert()
orbHealImage.set_colorkey((0,255,0))

enemyImage=pygame.image.load(path.join("images","enemy.png")).convert()
enemyImage.set_colorkey((0,255,0))

#################################
# FUNCTIONS #######################
#################################

#save game
def savelvl(game):
    world=game.gw
    ents=world.containing
    loc=path.join(world.levelname,"world"+str(world.pos[0])+str(world.pos[1])+".txt")
    if world:
        print world.player.prev
        #save stats
        f=open(path.join(world.playername,world.playername+".txt"),'w')
        #level,xp,nextxp,hp,maxhp,atk,gold,posx,posy,worldx,worldy,speed,kills
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
        allstuff+=str(world.player.speed)+"."
        allstuff+=str(world.player.kills)
        f.write(str(allstuff))
        f.close()

        #save quests
        f=open(path.join(world.playername,"que.sts"),'w')
        for q in game.qm.quests:
            f.write(str(q.id))
        f.close()

        #save inventory
        f=open(path.join(world.playername,"inv.txt"),'w')
        itemNum=0
        for a in world.player.inventory:
            #if itemNum+1!=len(world.player.inventory):
            f.write(str(world.player.inventory[itemNum].id)+"_"+str(world.player.inventory[itemNum].stack)+".")
            #else:
                #f.write(str(world.player.inventory[itemNum].id)+"_"+str(world.player.inventory[itemNum].stack))
            itemNum+=1
        f.write(str(world.player.activeWeapon[0].id)+"_a")
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

def startdungeon(index,w):
    faf=path.join(w.playername,w.game.ow.town+str(index))
    w.pos=[0,0]
    w.levelname=faf
    w.dungeonLevelCap=(5+index)+(index*w.game.ow.townIndex*4)
    print w.dungeonLevelCap
    w.player.reset()

    if path.isdir(faf):
        w.containing.empty()
        changelevel(w)
    else:
        print faf
        print w.levelname
        mkdir(faf)
        changelevel(w)


#draw a bar with %
def bar(surface,color1,color2,x,y,width,height,value,maxvalue):
    xx=0
    pygame.draw.rect(surface, color2, (x,y,width,height), 0)
    for hp in range(int(max(min(value / float(maxvalue) * width, width), 0))):
        pygame.draw.rect(surface, color1, (x+xx,y,1,height), 0)
        xx+= 1
    surface.blit(font.render(str(value)+"/"+str(maxvalue),0,(0,0,0)),(x+width/2-11,y+height/2-5))

#used to load into a new level
def changelevel(w):
    #change this to test if file exists
    w.containing.empty()
    loc=path.join(w.levelname,"world"+str(w.pos[0])+str(w.pos[1])+".txt")

    if path.isfile(loc):
        loadlvl(w.containing,loc)
        savelvl(w.game)
    else:
        fill(w.containing)
        carve(w.containing)
        doors(w.containing)
        savelvl(w.game)

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
        special=choice(([1]*11) #gold rate
                       +([2]*5)#enemy rate
                       +([3]*4)#random box rate
                       +([4]*2)#life drop rate
                       +([0]*111) #empty rate
                       )

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

        if special>0:
            rect = pygame.Rect(x,y,16,16)
            for ff in ents:
                if rect.colliderect(ff.rect):
                    ents.remove(ff)
            if special==1:
                ents.add(Pickup(x,y,"gold"))
            if special==2:
                ents.add(Enemy(x,y))
            if special==3:
                ents.add(Pickup(x,y,"randombox"))
            if special==4:
                ents.add(Pickup(x,y,"life"))

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
    #killhor
    rect = pygame.Rect(-5,224,900,2)
    for ff in ents:
        if rect.colliderect(ff.rect):
            ents.remove(ff)

    #killvert
    rect = pygame.Rect(384,-5,2,900)
    for ff in ents:
        if rect.colliderect(ff.rect):
            ents.remove(ff)

    ents.add(Door(768,224))
    ents.add(Door(384,480))
    ents.add(Door(384,0))
    ents.add(Door(0,224))


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



def LoadGame(w):
    playername=w.playername
    #levelname=w.levelname
    levelpath=path.join(playername)
    #ent=w.containing
    if path.isfile(path.join(playername,playername+".txt")):
        w.levelname=levelpath
        #load player attributes
        f=open(path.join(playername,playername+".txt"),'r')
        n=f.read()

        n=n.split(".")

        f.close()


        p=w.player
        #w.player=p
        #set attributes 4=gold
        #level,xp,nextxp,hp,maxhp,atk,gold,movespeed,kills
        p.setAttrs(n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[11],n[12])


        #loading inventory
        f=open(path.join(playername,"inv.txt"),'r')
        n2=f.read()
        f.close()

        #divide up by item
        n2=n2.split(".")
        if n2[0]!='':
            for f in n2:
                #divide up by name and stack
                f2=f.split("_")
                if f2[1]=='a':
                    p.activeWeapon=[items.fromId(int(f2[0]),p)]
                    break
                #give the item
                for f3 in range(int(f2[1])):
                    it=items.fromId(int(f2[0]),p)
                    p.giveItem(it)
    else:
        NewGame(w,True)

def NewGame(w,skip=False):
        playername=w.playername
        levelpath=path.join(playername)
        if path.isdir(playername):rmtree(playername)
        while path.isdir(playername):
            sleep(1)
        if not path.isdir(playername):
            w.levelname=levelpath
            mkdir(playername)
            #generate quests file
            f=open(path.join(playername,"que.sts"),'w');f.close()
            #mkdir(path.join(playername))

#################################
# CLASSES #######################
#################################


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class TextHolder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class PathNode:
    """
    Linked node representing a single movement in the pathfinding space.
    PathNode can be extended to provide different Cost and Fitness calculations.
    """
    MAX_FITNESS = 500

    def __init__(self, pos, prev_node, end_node):
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.prev = prev_node
        self.cost = self.calcCost(prev_node.rect.topleft, pos) + prev_node.cost if prev_node else 0
        self.fit = self.calcFitness(pos, end_node.rect.topleft) if end_node else PathNode.MAX_FITNESS

    def __cmp__(self, other):
        if self.rect.topleft == other.rect.topleft:
            return 0
        return cmp(self.fit, other.fit)

    def __hash__(self):
        return hash(self.rect.topleft)

    def __repr__(self):
        return "PathNode[%d] <%s> ->[%d] %d, %d" % (id(self), self.rect.topleft, id(self.prev), self.cost, self.fit)

    def calcCost(self, start, end):
        return mdistance(start, end)

    def calcFitness(self, start, end):
        return mdistance(start, end) + self.cost


class PathFinder:
    """
    An iterative path finder using the A* algorithm.
    An alternative Node Class can be specified to change the Fitness/Cost calculations.

    """

    def __init__(self, world, start, end, node_class=PathNode):
        print "PathFinder(%s, %s)" % (start, end)
        self.world = world
        self.nclass = node_class
        self.enode = node_class(end, None, None)
        self.snode = node_class(start, None, self.enode)
        self.closed = {}
        self.opened = {}
        self.sort = PriorityQueue()
        self.last = None
        self.nsteps = 0
        self.path = None

        # End node can't be a wall
        c = pygame.sprite.spritecollide(self.enode, world.containing, False)
        if c and c[0].name == "wall":
            self.path = [start]
            return self.path

        # Place start into open set
        self.opened[self.snode] = self.snode
        self.sort.put(self.snode)

    def processPath(self, steps=-1):
        # Check for solved path
        if self.path:
            return self.path

        current = None
        while steps != 0:
            if self.sort.empty():
                # Failed path points to start
                self.path = [self.snode.rect.topleft]
                break

            self.nsteps += 1
            steps -= 1

            current = self.sort.get()
            print "Pop[%d,%d] %s" % (self.sort.qsize(), len(self.opened), current)
            if current == self.enode:
                return self._constructPath(current)

            del self.opened[current]
            self.closed[current] = current
            nexts = (
                self.nclass((current.rect.left, current.rect.top-32), current, self.enode),
                self.nclass((current.rect.left+32, current.rect.top), current, self.enode),
                self.nclass((current.rect.left, current.rect.top+32), current, self.enode),
                self.nclass((current.rect.left-32, current.rect.top), current, self.enode),
            )

            for n in nexts:
                if n in self.closed:
                    continue

                c = pygame.sprite.spritecollide(n, self.world.containing, False)
                if c and c[0].name == "wall":
                    # Add walls to closed list to avoid checking them later
                    #print "\tWall %s" % n
                    self.closed[n] = n
                    continue

                m = self.opened.get(n, None)
                if not m:
                    # Add new node
                    #print "\tAdding %s" % n
                    self.opened[n] = n
                    self.sort.put(n)
                    continue
                else:
                    print "\tExisting %s as %s" % (n, m)

                if n.cost < m.cost:
                    # Replace old node with better node
                    print "\tReplacing %s with %s" % (m, n)
                    m.prev, m.cost = n.prev, n.cost

        self.last = current
        return self.path

    def draw(self, dsurf):
        """ Debug rendering of PathFinder info. """
        # Draw closed set
        for n in self.closed:
            pygame.draw.rect(dsurf, (255, 0, 0), n.rect, 1)

        # Draw open set
        for n in self.opened:
            pygame.draw.rect(dsurf, (128, 128, 0), n.rect, 2)
            fs = font.render(str(n.fit), 0, (255, 255, 255))
            dsurf.blit(fs, n.rect)
            fs = font.render(str(n.cost), 0, (128, 128, 128))
            dsurf.blit(fs, n.rect.center)

        if self.last:
            pygame.draw.rect(dsurf, (0, 255, 0), self.last.rect, 3)


    def update(self, steps=-1, dsurf=None):
        res = self.processPath(steps)
        if dsurf:
            self.draw(dsurf)
        return res

    def _constructPath(self, end):
        print "Constructing Path:"
        self.path = []
        while end.prev:
            print end
            self.path.insert(0, list(end.rect.topleft))
            end = end.prev
        return self.path


class Pickup(Entity):
    def __init__(self,x,y,ptype):
        Entity.__init__(self)
        self.name = "pickup"
        self.ptype = ptype
        self.image = Surface((32,32))
        self.image.convert()
        if self.ptype == "gold":
            self.name="gold"
            self.image=goldImage
        if self.ptype == "life":
            self.name="life"
            self.image=orbHealImage
        if self.ptype == "randombox":
            self.name="randombox"
            self.image=chestImage
        self.rect = Rect(x,y,32,32)



class Enemy(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "enemy"
        self.etype = "grunt"
        self.image = enemyImage
        self.rect = Rect(x,y,32,32)


class Wall(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "wall"
        self.image = wallImage
        #self.image.convert()
        #self.image.fill((100,100,100))
        self.rect = Rect(x,y,32,32)

class Door(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "door"
        self.image = Surface((1,1))
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

                wax=font.render(str("> "+self.drawntext[a]),0,(255,0,0),self.ic)
                surf.blit(wax,(self.rect.x+5,y))
                a+=1
                y+=12
