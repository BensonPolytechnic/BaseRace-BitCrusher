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

def andGate(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        sprite.fill([192, 192, 192], pygame.Rect([pixels / 12, pixels / 2], [(5 * pixels) / 6, (pixels / 2) - (pixels / 12)]))
        pygame.draw.circle(sprite, [192, 192, 192], [int(pixels / 2), int(pixels / 2)], int((5 * pixels) / 12), 0)
        return sprite
    
    elif state == 1:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        sprite.fill([232, 201, 71], pygame.Rect([pixels / 12, pixels / 2], [(5 * pixels) / 6, (pixels / 2) - (pixels / 12)]))
        pygame.draw.circle(sprite, [232, 201, 71], [int(pixels / 2), int(pixels / 2)], int((5 * pixels) / 12), 0)
        return sprite

def switch(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        sprite.fill([192, 192, 192], pygame.Rect([pixels / 4, pixels / 4], [pixels / 2, pixels / 2]))
        return sprite
    
    elif state == 1:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        sprite.fill([232, 201, 71], pygame.Rect([pixels / 4, pixels / 4], [pixels / 2, pixels / 2]))
        return sprite

def orGate(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.ellipse(sprite, [192, 192, 192], pygame.Rect([pixels / 12, pixels / 12], [(5 * pixels) / 6, (10 * pixels) / 6]), 0)
        sprite.fill([64, 64, 64], pygame.Rect([0, (11 * pixels) / 12], [pixels, pixels / 6]))
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 9) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        return sprite
    
    elif state == 1:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.ellipse(sprite, [232, 201, 71], pygame.Rect([pixels / 12, pixels / 12], [(5 * pixels) / 6, (10 * pixels) / 6]), 0)
        sprite.fill([64, 64, 64], pygame.Rect([0, (11 * pixels) / 12], [pixels, pixels / 6]))
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 9) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        return sprite

def xorGate(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.ellipse(sprite, [192, 192, 192], pygame.Rect([pixels / 12, pixels / 12], [(5 * pixels) / 6, (9 * pixels) / 6]), 0)
        sprite.fill([64, 64, 64], pygame.Rect([0, (10 * pixels) / 12], [pixels, pixels / 3]))
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 8) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        pygame.draw.ellipse(sprite, [192, 192, 192], pygame.Rect([pixels / 12, (pixels * 9) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 10) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        return sprite
    
    if state == 1:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.ellipse(sprite, [232, 201, 71], pygame.Rect([pixels / 12, pixels / 12], [(5 * pixels) / 6, (9 * pixels) / 6]), 0)
        sprite.fill([64, 64, 64], pygame.Rect([0, (10 * pixels) / 12], [pixels, pixels / 3]))
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 8) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        pygame.draw.ellipse(sprite, [232, 201, 71], pygame.Rect([pixels / 12, (pixels * 9) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 10) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        return sprite

def notGate(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.polygon(sprite, [192, 192, 192], [[pixels / 2, pixels / 6], [pixels / 12, (11 * pixels) / 12], [(11 * pixels) / 12, (11 * pixels) / 12]])
        pygame.draw.circle(sprite, [192, 192, 192], [int(pixels / 2), int(pixels / 6)], int(pixels / 12), 0)
        return sprite
    elif state == 1:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.polygon(sprite, [232, 201, 71], [[pixels / 2, pixels / 6], [pixels / 12, (11 * pixels) / 12], [(11 * pixels) / 12, (11 * pixels) / 12]])
        pygame.draw.circle(sprite, [232, 201, 71], [int(pixels / 2), int(pixels / 6)], int(pixels / 12), 0)
        return sprite

def hidden(pixels):
    sprite = pygame.Surface([pixels, pixels]).convert()
    sprite.fill([32, 32, 32])
    pygame.draw.line(sprite, [128, 128, 128], [0, 0], [pixels, pixels], 4)
    pygame.draw.line(sprite, [128, 128, 128], [0, pixels / 2], [pixels / 2, pixels], 4)
    pygame.draw.line(sprite, [128, 128, 128], [pixels / 2, 0], [pixels, pixels / 2], 4)
    
    return sprite

def sprite(id, pixels, state):
    if id == 0:
        return air(pixels, state)
    
    if id == 1:
        return weak(pixels, state)
    
    if id == 2:
        return medium(pixels, state)
    
    if id == 3:
        return strong(pixels, state)
    
    if id == 4:
        return andGate(pixels, state)
    
    if id == 5:
        return orGate(pixels, state)
    
    if id == 6:
        return xorGate(pixels, state)
    
    if id == 7:
        return notGate(pixels, state)
    
    if id == 8:
        return switch(pixels, state)
