#################################
# sam0s #######################
#################################

import pygame
from random import choice
from pygame import *
import battle,escmenu,items

pygame.init()
font=pygame.font.Font(None,15)

#menuimg=pygame.image.load("images\\menu.png")
#headshots=[pygame.image.load("images\\headshot1.png")]

#################################
# FUNCTIONS #######################
#################################


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
        allstuff+=str(world.pos[1])
        f.write(str(allstuff))
        f.close()

        #save inventory
        #f=open(world.playername+"\\""inv.txt",'w')
        #f.write(str(world.player.inventory[0]))
        #f.close()

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

def bar(surface,color1,color2,x,y,width,height,value,maxvalue):
    xx=0
    pygame.draw.rect(surface, color2, (x,y,width,height), 0)
    for hp in range(int(max(min(value / float(maxvalue) * width, width), 0))):
        pygame.draw.rect(surface, color1, (x+xx,y,1,height), 0)
        xx+= 1
    surface.blit(font.render(str(value)+"/"+str(maxvalue),0,(0,0,0)),(x+width/2-11,y+height/2-5))

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
    def __init__(self,containing,surf,hudsurf,images):
        self.images=images
        self.containing=containing
        self.turn=1
        self.pos=[0,0]
        self.player=None
        self.state="menu"
        self.surf=surf
        self.hudsurf=hudsurf
        self.hudlog=Log(self,439,1,360,125,(220,220,220),hudsurf)
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

    def Close(self,save=True):
        if save:
            savelvl(self.containing,self.levelname+"\\world"+str(self.pos[0])+str(self.pos[1])+".txt",self)
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
        if self.state == "menu":
            #menu routine
            self.hudsurf.fill((0,0,0))
            self.surf.blit(self.images[1],(0,0))
            pygame.display.flip()
            for e in self.events:
                if e.type==KEYUP:
                    if e.key==K_SPACE:
                        self.state="game"
                        self.Draw()
                        for f in range(20):
                            self.logtext.append(".")
                if e.type==QUIT:
                    self.Close(False)
        if self.state == "game":
            if self.good==1:
                if self.keys[K_TAB]:
                    self.esc.drawn=0
                    self.esc.created=0
                    self.ChangeState("escmenu")
            else:
                self.Draw()

            if not self.keys[K_TAB]:
                self.good=1

            for e in self.events:
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    print e.pos
                    #Headshot Click
                    if e.pos[0]<130:
                        if e.pos[1]>512:
                            self.esc.tab="player"
                            self.ChangeState("escmenu") #player tab
                if e.type == QUIT:
                    self.Close()

            self.player.update()

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
        self.surf.fill((0,0,0))
        if yesworld:
            self.containing.draw(self.surf)
        bar(self.hudsurf,(0,210,0),(210,0,0),130,4,165,25,self.player.hp,self.player.maxhp)
        bar(self.hudsurf,(75,0,130),(210,0,0),130,32,165,25,self.player.xp,self.player.nextxp)
        self.hudsurf.blit(self.images[2],(1,1))

    def Shift(self,d):
        savelvl(self.containing,self.levelname+"\\world"+str(self.pos[0])+str(self.pos[1])+".txt")
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

        changelevel(self.containing,self.levelname,self.pos)
        self.Draw()


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
        self.direct="w"
        self.inventory=[items.Bread(self)]
        self.activeWeapon=[items.Dirk(self)]

        self.changex=float(self.rect.x)
        self.changey=float(self.rect.y)

        

        #Stats
        self.level=1
        self.hp=100
        self.xp=0
        self.nextxp=120
        self.gold=0
        #Skills
        self.skillpoints=0
        self.atk=7
        self.speed=70
        self.maxhp=100

        

    def setAttrs(self,level,xp,nextxp,hp,maxhp,atk,gold):
        self.hp=int(hp)
        self.maxhp=int(maxhp)
        self.level=int(level)
        self.atk=int(atk)
        self.xp=int(xp)
        self.nextxp=int(nextxp)
        self.gold=int(gold)
    def giveItem(self,item):
        if len(self.inventory)==72:
            pass
        else:
            y=0
            for f in self.inventory:
                if f.name==item.name:
                    f.stack+=1
                    y=1
            if y==0:
                self.inventory.append(item)


    def levelUp(self,rollover=0):
        #LEVEL UP
        self.level+=1
        self.atk+=(self.level+3)
        #CHANGE THIS LATER
        self.nextxp+=150
        if rollover>0:
            self.giveXp(rollover)

    def giveXp(self,xp):
        if xp>=self.nextxp:
            xp=xp-self.nextxp
            self.levelUp(xp)
        else:
            self.xp+=xp



    def update(self):
        pygame.draw.rect(self.world.surf,(0,255,0),(self.rect.x,self.rect.y,32,32),0)
        #print self.activeWeapon[0].ad
        #print self.inventory

        if not self.moving:
            self.prev=[self.rect.x,self.rect.y]
            k=self.world.keys
            if k[K_w]:
                self.direct="w"
                self.moveto[1]-=32
                self.wasd=0
                self.moving=True
            elif k[K_a]:
                self.direct="a"
                self.moveto[0]-=32
                self.wasd=0
                self.moving=True
            elif k[K_s]:
                self.direct="s"
                self.moveto[1]+=32
                self.wasd=0
                self.moving=True
            elif k[K_d]:
                self.direct="d"
                self.moveto[0]+=32
                self.wasd=0
                self.moving=True
            if self.moving == True:
                self.changex=float(self.prev[0])
                self.changey=float(self.prev[1])
        else:
            #collision
            cl=pygame.sprite.spritecollide(self, self.world.containing, False)
            if cl:
                self.world.esc.created=0
                for f in cl:
                    if f.name=='door':
                        if self.rect.y<64:
                            self.world.Shift('n')
                        elif self.rect.x>704:
                            self.world.Shift('e')
                        elif self.rect.y>416:
                            self.world.Shift('s')
                        elif self.rect.x<64:
                            self.world.Shift('w')
                    if f.name=='enemy':
                        self.world.logtext.append("Enemy Encounter!")
                        self.world.bat.NewEnemy()
                        self.world.battle=True
                        self.world.ChangeState("battle")
                        self.world.containing.remove(f)
                    if f.name=='gold':
                        #self.giveXp(3+self.level*2)
                        self.giveXp(1000)
                        self.world.logtext.append("gold found!")
                        self.world.containing.remove(f)
                        savelvl(self.world.containing,self.world.levelname+"\\world"+str(self.world.pos[0])+str(self.world.pos[1])+".txt")
                        self.gold+=1
                    if f.name=='life':
                        self.world.containing.remove(f)
                        self.world.logtext.append("health found!")
                        self.hp+=25
                        if self.hp>self.maxhp:
                            self.hp=self.maxhp
                    if f.name=="randombox":
                        #Give a random item from this here list !
                        randomitem=choice([1,2,3,4,5,6])
                        self.giveItem(items.fromId(randomitem,self))
                        self.world.containing.remove(f)


                    if f.name=='wall':
                        self.moveto=self.prev
                    self.world.Draw()



            #move based on time delta
            if self.rect.x<self.moveto[0]:
                self.changex+=(self.speed)*self.world.delta
                if self.changex>self.moveto[0]-1:self.changex=self.moveto[0]
            elif self.rect.x>self.moveto[0]:
                self.changex-=(self.speed)*self.world.delta
                if self.changex<self.moveto[0]+1:self.changex=self.moveto[0]
            elif self.rect.y<self.moveto[1]:
                self.changey+=(self.speed)*self.world.delta
                if self.changey>self.moveto[1]+1:self.changey=self.moveto[1]
            elif self.rect.y>self.moveto[1]:
                self.changey-=(self.speed)*self.world.delta
                if self.changey<self.moveto[1]-1:self.changey=self.moveto[1]
            else:
                self.moving=False
                self.world.Draw()


            pygame.draw.rect(self.world.surf,(0,255,0),(self.rect.x,self.rect.y,32,32),0)

            #blackster
            if self.direct=="w":
                pygame.draw.rect(self.world.surf,(0,0,0),(self.rect.x,self.rect.y+32,32,2),0)
            if self.direct=="a":
                pygame.draw.rect(self.world.surf,(0,0,0),(self.rect.x+32,self.rect.y,2,32),0)
            if self.direct=="s":
                pygame.draw.rect(self.world.surf,(0,0,0),(self.rect.x,self.rect.y-2,32,2),0)
            if self.direct=="d":
                pygame.draw.rect(self.world.surf,(0,0,0),(self.rect.x-2,self.rect.y,2,32),0)

            self.rect.x=int(self.changex)
            self.rect.y=int(self.changey)


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
