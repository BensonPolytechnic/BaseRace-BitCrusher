#blocksprites.py

import pygame
from pygame.locals import *

def air(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([223, 223, 223])
        sprite.fill([255, 255, 255], pygame.Rect([pixels / 40, pixels / 40], [pixels - (pixels / 20), pixels - (pixels / 20)]))
        return sprite

def weak(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([255, 210, 128])
        return sprite

def medium(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([157, 51, 0])
        return sprite

def strong(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([133, 107, 107])
        return sprite

def goo(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([192, 255, 192])
        return sprite
