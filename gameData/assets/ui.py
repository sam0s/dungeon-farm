#!/usr/bin/env python

"""
ui.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []



import pygame
from random import choice
from pygame import *
from os import path
pygame.init()


fontpath=path.split(path.realpath("ui.py"))
fontpath=path.join(fontpath[0],"digfont.ttf")
print fontpath
font=pygame.font.Font(fontpath,11)


def LoadFont():
    return font

class UiObj(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Button(UiObj):
    def __init__(self,x,y,sizex,sizey,text,surf):
        UiObj.__init__(self)
        self.text=text
        self.image=pygame.Surface((sizex,sizey))
        self.image.fill((255,0,0))
        self.rect=Rect(x,y,sizex,sizey)
        self.surf=surf
        self.textimg=font.render(text,0,(255,255,255))
    def Update(self):
        self.surf.blit(self.image,(self.rect.x,self.rect.y))
        self.surf.blit(self.textimg,((self.rect.x+(self.rect.right-self.rect.left)/2) - self.textimg.get_width()/2, (self.rect.y+(self.rect.bottom-self.rect.top)/2) - self.textimg.get_height()/2))
