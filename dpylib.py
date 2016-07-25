#dungeonpy library
import pygame
from random import choice
from pygame import *

pygame.init()
font=pygame.font.Font(None,15)
hudbord = pygame.image.load("hudborder.png")

def savelvl(ents,loc):
    save = open(loc,"w")
    for f in ents:
        save.write('"'+f.name+'"'+"."+str(f.rect.left)+"."+str(f.rect.top)+".")
    save.close()

def loadlvl(ents,loc):
    load = open(loc,"r")
    read = 0
    data = load.read()
    data=data.split(".")
    data=data[:-1]
    while len(data) > 0:
        if data[0]=='"wall"':
            w=Wall(int(data[1]),int(data[2]))
        if data[0]=='"player"':
            w=Player(int(data[1]),int(data[2]))
        ents.add(w)
        data=data[3:]
    load.close()

def bar(surface,color1,color2,x,y,width,height,value,maxvalue):
    xx=0
    pygame.draw.rect(surface, color2, (x,y,width,height), 0)
    for hp in range(int(max(min(value / float(maxvalue) * width, width), 0))):
        pygame.draw.rect(surface, color1, (x+xx,y,1,height), 0)
        xx+= 1

def changelevel(ents,loc,pos):
    try:
        ents.empty()
        loadlvl(ents,loc+"\\world"+str(pos[0])+str(pos[1])+".txt")
    except:
        fill(ents)
        carve(ents)
        savelvl(ents,loc+"\\world"+str(pos[0])+str(pos[1])+".txt")


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
        while direction == lastdir:
            direction = choice([1,2,3,4])
        lastdir = direction
        if direction == 1:
            for f in range(choice([3,4,5,9,15])):
                if x<736: x+=32
                rect = pygame.Rect(x,y,16,16)
                for ff in ents:
                    if rect.colliderect(ff.rect):
                        ents.remove(ff)
        if direction == 2:
            for f in range(choice([3,4,5,9,15])):
                if x>32: x-=32
                rect = pygame.Rect(x,y,16,16)

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
                rect = pygame.Rect(x,y,16,16)

                for ff in ents:
                    if rect.colliderect(ff.rect):
                        ents.remove(ff)
def fill(ents):
    x=y=0
    while y < 510:
        while x < 800:
            w=Wall(x,y)
            ents.add(w)
            x+=32
        x=0
        y+=32

def drawhud(asurf):
    asurf.blit(hudbord,(0,0))


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Wall(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "wall"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((100,100,100))
        self.rect = Rect(x,y,32,32)
class Player(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "player"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((0,250,0))
        self.rect = Rect(x,y,32,32)
        self.wasd=0
    def update(self,surf):
        px=self.rect.x
        py=self.rect.y
        k=pygame.key.get_pressed()
        if not k[K_w] and not k[K_a] and not k[K_s] and not k[K_d]:
            self.wasd=1
        if self.wasd==1:
            if k[K_w]:
                self.rect.y-=32
                self.wasd=0
            if k[K_a]:
                self.rect.x-=32
                self.wasd=0
            if k[K_s]:
                self.rect.y+=32
                self.wasd=0
            if k[K_d]:
                self.rect.x+=32
                self.wasd=0
        if surf.get_at((self.rect.x+16,self.rect.y+16)) != (0,0,0):
            self.rect.x=px
            self.rect.y=py
        pygame.draw.rect(surf,(0,255,0),(self.rect.x,self.rect.y,32,32),2)
