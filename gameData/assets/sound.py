#!/usr/bin/env python

"""
sound.py

"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []



import pygame
from random import choice
from pygame import *
from os import path

pygame.init()

class Mix(object):
    def __init__(self):
        self.sounds=sounds = {"button":pygame.mixer.Sound(path.join("sound","popupmessage.wav"))}
    def Play(self,sndname):
        self.sounds[sndname].play()
