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

pygame.mixer.init(frequency=22050, size=-16, channels=4, buffer=4096)

class Mix(object):
    def __init__(self):
        self.sounds=sounds = {"button":pygame.mixer.Sound(path.join("sound","popupmessage.wav"))}
    def Play(self,sndname):
        self.sounds[sndname].stop()
        self.sounds[sndname].play()
