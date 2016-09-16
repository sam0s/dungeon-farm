import pygame
from random import choice
from pygame import *

pygame.init()
font=pygame.font.Font(None,15)

class UiObj(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Button(UiObj):
    def __init__(self,x,y,sizex,sizey,text,surf):
        UiObj.__init__(self)
        self.image=pygame.Surface((sizex,sizey))
        self.image.fill((255,0,0))
        self.rect=Rect(x,y,sizex,sizey)
        self.surf=surf
        self.textimg=font.render(text,0,(255,255,255))
    def Update(self):
        self.surf.blit(self.image,(self.rect.x,self.rect.y))
        self.surf.blit(self.textimg,((self.rect.x+(self.rect.right-self.rect.left)/2) - self.textimg.get_width()/2, (self.rect.y+(self.rect.bottom-self.rect.top)/2) - self.textimg.get_height()/2))
        
        
