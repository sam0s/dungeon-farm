#################################
# sam0s #######################
#################################


import pygame
from random import choice
from pygame import *

pygame.init()
font=pygame.font.Font(None,15)

#################################
# FUNCTIONS #######################
#################################

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
        if data[0]=='"door"':
            w=Door(int(data[1]),int(data[2]))
        if data[0]=='"gold"':
            w=Gold(int(data[1]),int(data[2]))
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
        doors(ents)
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
        special=choice([1,0,0,0,0,0,0,0,0,0])
        if special==1:
            ents.add(Gold(x,y))
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
def fill(ents):
    x=y=0
    while y < 510:
        while x < 800:
            w=Wall(x,y)
            ents.add(w)
            x+=32
        x=0
        y+=32
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



#################################
# CLASSES #######################
#################################


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
class TextHolder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class World(object):
    def __init__(self,containing):
        self.containing=containing
        self.turn=1
        self.pos=[0,0]
        self.player=None
    def SetPlayer(self,p):
        self.player=p
    def Turn(self):
        self.turn+=1
        if self.turn%2 ==0:
            #turn
            pass
    def Update(self,surf):
        surf.fill((0,0,0))
        self.containing.draw(surf)
    def Shift(self,d,surf):
        global logtext
        if d=='n':
            self.pos=[self.pos[0],self.pos[1]-1]
            self.player.moveto[1]=self.player.rect.y=448
            
            logtext.append("going north")
        elif d=='e':
            self.pos=[self.pos[0]+1,self.pos[1]]
            self.player.moveto[0]=self.player.rect.x=32

            logtext.append("going east")
        elif d=='s':
            self.pos=[self.pos[0],self.pos[1]+1]
            self.player.moveto[1]=self.player.rect.y=32

            logtext.append("going south")
        elif d=='w':
            self.pos=[self.pos[0]-1,self.pos[1]]
            self.player.moveto[0]=self.player.rect.x=736

            logtext.append("going west")
        changelevel(self.containing,"lvl",self.pos)
        self.Update(surf)


class Gold(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.name = "gold"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((255,255,0))
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

class Player(Entity):
    def __init__(self,x,y,world):
        Entity.__init__(self)
        self.world=world
        self.name = "player"
        self.image = Surface((32,32))
        self.image.convert()
        self.image.fill((0,250,0))
        self.rect = Rect(x,y,32,32)
        self.prev = self.moveto = [x,y]
        self.moving=False
        self.prev=[]
        self.worldpos=[0,0]
    def update(self,surf):
        if not self.moving:
            self.prev=[self.rect.x,self.rect.y]
            k=pygame.key.get_pressed()
            if k[K_w]:
                self.moveto[1]-=32
                self.wasd=0
                self.moving=True
            elif k[K_a]:
                self.moveto[0]-=32
                self.wasd=0
                self.moving=True
            elif k[K_s]:
                self.moveto[1]+=32
                self.wasd=0
                self.moving=True
            elif k[K_d]:
                self.moveto[0]+=32
                self.wasd=0
                self.moving=True
            if self.moving == True:
                self.world.Turn()
        else:

            #collision
            cl=pygame.sprite.spritecollide(self, self.world.containing, False)
            if cl:
                for f in cl:
                    if f.name=='door':
                        if self.rect.y<64:
                            self.world.Shift('n',surf)
                        elif self.rect.x>704:
                            self.world.Shift('e',surf)
                        elif self.rect.y>416:
                            self.world.Shift('s',surf)
                        elif self.rect.x<64:
                            self.world.Shift('w',surf)
                    if f.name=='gold':
                        pygame.sprite.spritecollide(self, self.world.containing, True)
                    if f.name=='wall':
                        self.moveto=self.prev
            self.world.Update(surf)
            if self.rect.x<self.moveto[0]: self.rect.x+=2
            elif self.rect.x>self.moveto[0]: self.rect.x-=2
            elif self.rect.y<self.moveto[1]: self.rect.y+=2
            elif self.rect.y>self.moveto[1]: self.rect.y-=2
            else: self.moving=False
            
        pygame.draw.rect(surf,(0,255,0),(self.rect.x,self.rect.y,32,32),0)

class Log(TextHolder):
    def __init__(self,x,y,sizex,sizey,ic,surf):
        TextHolder.__init__(self)
        self.rect=pygame.Rect(x,y,sizex,sizey)
        global logtext
        logtext=[]
        #INNER AND OUTER COLORS
        self.ic=ic
        self.oc=(0,0,0)
        self.textY=4
        pygame.draw.rect(surf,(self.ic),self.rect,0)
        pygame.draw.rect(surf,(self.oc),self.rect,3)
    def update(self,surf):
        global logtext
        if len(logtext)>0:
            for f in logtext:
                if self.textY<112:self.textY+=12
                else:self.textY=4;pygame.draw.rect(surf,(self.ic),self.rect,0);pygame.draw.rect(surf,(self.oc),self.rect,3)
                wax=font.render(str(logtext[0]),0,(255,0,0))
                surf.blit(wax,(4,self.textY))
                logtext=logtext[1:]

            
            
            
            
        
