#!/usr/bin/env python
"""
items. py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []

class Item:
    def __init__(self):
        self.stack=1
    def setContainer(self,setpc):
        self.parentContain=setpc
    def setName(self, name):
        self.name = name
    def destroy(self):
        test=self.parentContain
        print self.name
    def Use(self):
        if isinstance(self,Food):
            print self.parentContain.index(self)
            self.parent.food-=self.consumeVal

#TYPES

#EAT
class Apple(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name="apple"
        self.consumeVal = 15
        self.weight = 1
        self.stack=1
        self.imgnum=0
class Bread(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name="bread"
        self.consumeVal = 20
        self.weight = 1
        self.stack=1
        self.imgnum=0
class OrcSteak(Item):
    def __init__(self,setp,setpc=None):
        self.parent=setp
        self.parentContain=setpc
        self.name="orc steak"
        self.consumeVal = 25
        self.weight = 1
        self.stack=1
        self.imgnum=0







