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



def LoadFont(size=11):
    fontpath=path.split(path.realpath("ui.py"))
    print fontpath
    fontpath=path.join(fontpath[0],"digfont.ttf")
    print fontpath
    fonst=pygame.font.Font(fontpath,size)
    return fonst

uiF=LoadFont(13)

class UiObj(pygame.sprite.Sprite):
    def __init__(self,text,rect,surf):
        pygame.sprite.Sprite.__init__(self)
        self.text=text
        self.rect=rect
        self.surf=surf

class Button(UiObj):
    def __init__(self,x,y,sizex,sizey,text,surf):
        UiObj.__init__(self,text,Rect(x,y,sizex,sizey),surf)
        self.image=pygame.Surface((sizex,sizey))
        self.image.fill((255,0,0))
        self.textimg=uiF.render(text,0,(255,255,255))
    def Update(self):
        self.surf.blit(self.image,(self.rect.x,self.rect.y))
        self.surf.blit(self.textimg,((self.rect.x+(self.rect.right-self.rect.left)/2) - self.textimg.get_width()/2, (self.rect.y+(self.rect.bottom-self.rect.top)/2) - self.textimg.get_height()/2))

class CheckBox(UiObj):
    def __init__(self,x,y,text,surf,size=32):
        UiObj.__init__(self,text,Rect(x,y,32,32),surf)
        self.size=size
        self.image=pygame.Surface((size,size))
        pygame.draw.rect(self.image,(255,0,0),(0,0,size,size),1)
        self.active=False
        self.textimg=uiF.render(text,0,(255,255,255))
    def Check(self):
        if self.active==False:
            self.active=True
            return self.active
        if self.active==True:
            self.active=False
            return self.active
    def Update(self):

        self.surf.blit(self.image,(self.rect.x,self.rect.y))
        a=(self.rect.x+(self.rect.right-self.rect.left)/2) - self.textimg.get_width()/2
        self.surf.blit(self.textimg,(a,self.rect.y+self.size+6))
        if self.active:
            pygame.draw.circle(self.surf,(0,0,255),(self.rect.x+self.size/2,self.rect.y+self.size/2),8,0)
