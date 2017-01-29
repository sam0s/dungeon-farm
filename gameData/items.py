#!/usr/bin/env python

"""
items. py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []

import pygame

itemsheet = pygame.image.load("images\\item.png")

class Item:
    def __init__(self):
        self.stack=1
    def setContainer(self,setpc):
        self.parentContain=setpc
    def setName(self, name):
        self.name = name
    def destroy(self):
        self.parent.inventory.remove(self)

#TYPES


#WEAPON
class Dirk(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.itemType="weapon"
        self.name="dirk"

        self.id = 0

        self.val = 15
        self.consumeVal = 0
        self.ad = 10
        self.ap = 0
        self.weight = 1

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(self.id*26, 0, 26, 26))

#EAT
class Bread(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.itemType="food"

        self.id=1

        self.val=5
        self.name="bread"
        self.consumeVal = 20
        self.ad=0
        self.ap=0
        self.weight = 0.5

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(self.id*26, 0, 26, 26))



class Apple(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.itemType="food"

        self.id=2

        self.val = 2
        self.name="apple"
        self.consumeVal = 15
        self.ad = 0
        self.ap = 0
        self.weight = 1

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(self.id*26, 0, 26, 26))


class Pizza(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.itemType="food"

        self.id=3

        self.val = 2
        self.name="pizza"
        self.consumeVal = 25
        self.ad = 0
        self.ap = 0
        self.weight = 1

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(self.id*26, 0, 26, 26))

class Cheese(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.itemType="food"

        self.id=4

        self.val = 2
        self.name="cheese"
        self.consumeVal = 10
        self.ad = 0
        self.ap = 0
        self.weight = 1

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(self.id*26, 0, 26, 26))

class Fish(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.itemType="food"

        self.id=5

        self.val = 2
        self.name="fish"
        self.consumeVal = 15
        self.ad = 0
        self.ap = 0
        self.weight = 1

        self.stack=1

        self.image = itemsheet.subsurface(pygame.Rect(self.id*26, 0, 26, 26))

def fromId(idn,parent):
    if idn==1:
        return Bread(parent)
    if idn==2:
        return Apple(parent)
    if idn==3:
        return Pizza(parent)
    if  idn==4:
        return Cheese(parent)
    if idn==5:
        return Fish(parent)
