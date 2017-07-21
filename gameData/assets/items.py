#!/usr/bin/env python

"""
items.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []

import pygame
from os import path
from random import choice

itemsheet = pygame.image.load(path.join("images","itemF.png")).convert()
itemsheetWeapon = pygame.image.load(path.join("images","itemW.png")).convert()
itemsheetQuest = pygame.image.load(path.join("images","itemQ.png")).convert()


class Item:
    def __init__(self):
        self.stack=1

####### QUEST ITEMS ##########
###########################
class Gabe(Item):
    def __init__(self):
        self.itemType="quest"
        self.name="gabe"
        self.descr=["A cute dog named Gabe! He belongs to a man from Fairfield."]
        self.id = 100

        self.val = 15
        self.consumeVal = 0
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheetQuest.subsurface(pygame.Rect(0*26, 0, 26, 26)).convert()

class CherishedBow(Item):
    def __init__(self):
        self.itemType="quest"
        self.name="cherishedbow"
        self.descr=["A sacred bow. It once belonged to a leader of","the Quiet Bison tribe, far to the west."]

        self.id = 101

        self.val = 100
        self.consumeVal = 0
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheetQuest.subsurface(pygame.Rect(1*26, 0, 26, 26)).convert()

class Drum(Item):
    def __init__(self):
        self.itemType="quest"
        self.name="drum"
        self.descr=["This sacred drum belongs to the Bright Foot tribe."]

        self.id = 102
        
        self.val = 100
        self.consumeVal = 0
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheetQuest.subsurface(pygame.Rect(2*26, 0, 26, 26)).convert()

############ WEAPONS #######################
##########################
class Dirk(Item):
    def __init__(self):
        self.itemType="weapon"
        self.name="dirk"
        self.descr=["A very standard dirk.","","AD - 7"]

        self.id = 200

        self.val = 15
        self.consumeVal = 0
        self.ad = 7
        self.ap = 0

        self.stack=1

        self.image = itemsheetWeapon.subsurface(pygame.Rect(0*26, 0, 26, 26)).convert()

class Sword(Item):
    def __init__(self):
        self.itemType="weapon"
        self.name="sword"
        self.descr=["A two handed steel blade.","","AD - 12"]
        self.id = 201

        self.val = 25
        self.consumeVal = 0
        self.ad = 12
        self.ap = 0

        self.stack=1

        self.image = itemsheetWeapon.subsurface(pygame.Rect(1*26, 0, 26, 26)).convert()

## EAT ##
#########
class Bread(Item):
    def __init__(self):
        self.itemType="food"
        self.descr=["Some tasty bread.","","Heals for - 20"]
        self.id=1

        self.val=5
        self.name="bread"
        self.consumeVal = 20
        self.ad=0
        self.ap=0

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(1*26, 0, 26, 26)).convert()



class Apple(Item):
    def __init__(self):
        self.itemType="food"
        self.descr=["A ripe red apple.","","Heals for - 15"]
        self.id=2

        self.val = 2
        self.name="apple"
        self.consumeVal = 15
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(2*26, 0, 26, 26)).convert()

class Porkchop(Item):
    def __init__(self):
        self.itemType="food"
        self.descr=["A well cooked porkchop.","","Heals for - 25"]
        self.id=3

        self.val = 2
        self.name="pizza"
        self.consumeVal = 25
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(3*26, 0, 26, 26)).convert()

class Cheese(Item):
    def __init__(self):
        self.itemType="food"
        self.descr=["Some funny smelling cheese.","","Heals for - 10"]
        self.id=4

        self.val = 2
        self.name="cheese"
        self.consumeVal = 10
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(4*26, 0, 26, 26)).convert()

class Fish(Item):
    def __init__(self):
        self.itemType="food"
        self.descr=["A fish, ready to be eaten.","","Heals for - 15"]
        self.id=5

        self.val = 2
        self.name="fish"
        self.consumeVal = 15
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(5*26, 0, 26, 26)).convert()

class HealthPotion(Item):
    def __init__(self):
        self.itemType="food"
        self.descr=["A minor potion of healing, brewed to perfection.","","Heals for - 50"]
        self.id=6

        self.val = 2
        self.name="healthpot"
        self.consumeVal = 50
        self.ad = 0
        self.ap = 0

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(6*26, 0, 26, 26)).convert()

def fromId(idn,parent=None,justname=False):
    print idn

    itemDict= {1:"Bread",
               2:"Apple",
               3:"Porkchop",
               4:"Cheese",
               5:"Fish",
               6:"HealthPotion",
               200:"Dirk",
               201:"Sword",
               100:"Gabe",
               101:"CherishedBow",
               102:"Drum"
               }
    if not justname:
        return eval(itemDict[idn]+"()")
    return itemDict[idn]

def randomItem():
    #incorporate levels
    randomIDN=choice(([1]*12) #bread
                   +([2]*15) #apple
                   +([3]*14) #porkchop
                   +([4]*13) #cheese
                   +([5]*13) #fish
                   +([6]*8) #hpot
                   +([201]*4) #sword
                   )
    return fromId(randomIDN)
