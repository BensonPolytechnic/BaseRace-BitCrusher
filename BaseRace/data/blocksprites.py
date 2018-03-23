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

def orGate(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.ellipse(sprite, [192, 192, 192], pygame.Rect([pixels / 12, pixels / 12], [(5 * pixels) / 6, (10 * pixels) / 6]), 0)
        sprite.fill([64, 64, 64], pygame.Rect([0, (11 * pixels) / 12], [pixels, pixels / 6]))
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 9) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        return sprite

def xorGate(pixels, state):
    if state == 0:
        sprite = pygame.Surface([pixels, pixels]).convert()
        sprite.fill([64, 64, 64])
        pygame.draw.ellipse(sprite, [192, 192, 192], pygame.Rect([pixels / 12, pixels / 12], [(5 * pixels) / 6, (10 * pixels) / 6]), 0)
        sprite.fill([64, 64, 64], pygame.Rect([0, (11 * pixels) / 12], [pixels, pixels / 6]))
        pygame.draw.ellipse(sprite, [64, 64, 64], pygame.Rect([pixels / 12, (pixels * 9) / 12], [(5 * pixels) / 6, pixels / 3]), 0)
        return sprite