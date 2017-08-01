#!/usr/bin/env python

"""
Enemies.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []

import pygame
from random import choice,randint
from os import path

#MAKE THIS A SUBSURFACE SET LATER
orcHeadshot=pygame.image.load(path.join("images","headshots","orcheadshot.png"))
goblinHeadshot=pygame.image.load(path.join("images","headshots","goblinheadshot.png"))
testHeadshot=pygame.image.load(path.join("images","gold.png"))

class Enemy:
    def __init__(self):
        self.stack=1
    def Attack(self):
        #enemy damage algorithim
        dmg=self.atk+self.level*2
        dmg=(randint(0,5*dmg))/6
        return dmg

#TYPES

class BadDude(Enemy):
    def __init__(self,level):
        self.atk=11
        self.level=level
        self.hp=self.maxhp=self.level*17
        self.name="testEnemy"
        self.image=testHeadshot.convert()

class Orc(Enemy):
    def __init__(self,level):
        self.atk=11
        self.level=level
        self.hp=self.maxhp=self.level*17
        self.name="orc"
        self.image=orcHeadshot.convert()

class Goblin(Enemy):
    def __init__(self,level):
        self.atk=8
        self.level=level
        self.hp=self.maxhp=self.level*15
        self.name="goblin"
        self.image=goblinHeadshot.convert()



def fromId(idn,parent,justname=False):

    if idn==1:
        if not justname:
            return Bread(parent)
        return "Bread"
    if idn==2:
        if not justname:
            return Apple(parent)
        return "Apple"
    if idn==3:
        if not justname:
            return Pizza(parent)
        return "Pizza"
    if  idn==4:
        if not justname:
            return Cheese(parent)
        return "Cheese"
    if idn==5:
        if not justname:
            return Fish(parent)
        return "Fish"
    if idn==6:
        if not justname:
            return HealthPot(parent)
        return "Health Potion"
