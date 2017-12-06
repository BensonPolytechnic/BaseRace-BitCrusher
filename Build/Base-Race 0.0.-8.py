'''
base race non-functional build
'''

# IMPORTS #
import pygame
from pygame.locals import *
from math import atan
# SETUPS #
pygame.init()

# screen size
screen = (1920,1080)

# sizing things
blockSize = 32
playerRadius = 8

# client to server variables
gameStart = False
up = False
down = False
left = False
right = False
shoot = False
degree = 0

#COLORS#
BLUE = (0,170,255)
ORANGE = (255,170,0)
BEIGE = (255,240,200)
GREY = (170,170,170)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (140,210,70)

# sets up client-server connection
serverIp = input("Game Server IP: ")
port = 25565 # I like building brown bricks with minecraft
# walkers coolio client stuff

# start window
win = pygame.display.set_mode(screen,pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

# LEVEL FILE #
layout = open('BasicWorld.txt', 'r')

rectList = []

def buildWorld():
    row = 0
    world = layout.read().split('\n')
    for r in world:
        col = 0
        for c in r:
            if c != 'N':
                rectList.append(pygame.Rect((c * blockSize), (r * blockSize), blockSize, blockSize))
            col += blockSize
        row += blockSize
                    
def main():
    # IMPORTANT MAIN LOOP #
    while True:
        for event in pygame.event.get():
            
            # events go here
            if event.type == pygame.QUIT:
                return
            
            # keystrokes go here
            key = pygame.key.get_pressed()
            # quit
            if key[pygame.K_ESCAPE]:
                return
            # WASD
            if key[pygame.K_w]:
                up()
            if key[pygame.K_a]:
                left()
            if key[pygame.K_s]:
                down()
            if key[pygame.K_d]:
                right()
            
            # mouse handler
            mouse = pygame.mouse.get_pressed()
            # shooting
            if mouse[0]:
                shoot = True
                # shoot angle
                mousePos = pygame.mouse.get_pos()
                adj = ((screen[0] / 2) - mousePos[0])
                opp = ((screen[1] / 2) - mousePos[1])
                # get quadrant to find total angle
                if adj >= 0 and opp > 0:
                    q = 0
                elif adj <= 0 and opp > 0:
                    q = 1
                elif adj <= 0 and opp < 0:
                    q = 2
                elif adj <= 0 and opp < 0:
                    q = 3
                elif adj < 0 and opp == 0:
                    degree = 180
                elif adj > 0 and opp == 0:
                    degree = 0
                
                # no try except crashes here
                if adj == 0:
                    # CATCH THAT DIVISION BY ZERO SON
                    degree = 90 * q
                else:
                    degree = round(math.degrees(math.atan(abs(opp)/abs(adj))) + (90 * q), 4)

main()
pygame.quit()