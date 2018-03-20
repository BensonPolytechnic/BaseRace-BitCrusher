# *** GRAPHICS ENGINE ***
# This is a thing that makes pixels on a screen turn pretty colors

import pygame, os, time, math
from pygame.locals import *

pygame.init()
pygame.font.init()

# Takes a position of a point in the world, and returns its position on the screen in pixels.
def getScreenPos(pos):
    return [int((pos[0] - cameraPos[0] + (cameraZoom / 2)) * ((scrW / cameraZoom))), int((pos[1] - cameraPos[1] + (cameraZoom * (scrH / scrW)) / 2) * (scrW / cameraZoom))]

# Takes a position of something on the screen in pixels, and returns its position in the world.

def quadraticSolutions(a, b, c):
    return [((-b) + math.sqrt(math.pow(b, 2) - 4 * a * c)) / (2 * a), ((-b) - math.sqrt(math.pow(b, 2) - 4 * a * c)) / (2 * a)]

# This takes a point, a slope ("+inf" for straight up and "-inf" for straight down), and a direction (-1 for towards -x, 1 for towards x, and 0 for neither)
# and returns the nearest point of intersection of that ray with an object in the world, a player, or the edge of the world.
# The variables offSetX, offSetY, xInt, yInt, stepX, and stepY show up throughout this function.
# I'm not going to re-describe what they're doing every time they show up so I'm just going to put their description here:

# xInt - Nearest vertical intersection with the world's grid.

# yInt - Nearest horizontal intersection with the world's grid.

# offSetX - Annoying thing used to make variables round correctly.

# offSetY - Another annoying thing used to make variables round correctly.

# stepX - Increments xInt[0], used to check the next position in the world for a collision.

# stepY - Increments yInt[1], used to check the next position in the world for a collision.

# The operation of this entire function is difficult to explain with words alone, because it's based on a bunch of complicated and annoying math.
# If you need to know how stuff works in here, talk to me.

def raycast(point, slope, dir=0, team=None):
    collisions = []
    
    # If the slope is 0, this performs a simplified version of the calculations that don't screw around with yInt.
    if slope == 0:
        
        # Detects collisions with players.
        # Only checks for collisions with the players on the other team.
        for player in players:
            if player["team"] == team:
                continue
            
            elif point[1] <= player["pos"][1] + 0.5 and point[1] >= player["pos"][1] - 0.5:
                collisions.append([player["pos"][0], point[1]])
        
        if dir > 0:
            offSetX = 0
            stepX = 1
            xInt = [int(point[0]) + 1, point[1]]
            
        else:
            offSetX = -1
            stepX = -1
            xInt = [int(point[0]), point[1]]
            
        while True:
            if xInt[0] >= worldSize[0] + offSetX or xInt[0] <= 0:
                collisions.append(xInt)
                break
            elif world[xInt[0] + offSetX][int(xInt[1])]["type"] != 0 or xInt[0] >= worldSize[0] + offSetX or xInt[0] <= 0:
                collisions.append(xInt)
                break
            
            else:
                xInt[0] += stepX
    
    # If the ray is pointing straight up, this performs a simplified version of the calculations that don't screw around with xInt.
    elif slope == "+inf":
        
        # Detects collisions with players.
        # Only checks for collisions with the players on the other team.
        for player in players:
            if player["team"] == team:
                continue
            
            elif point[0] <= player["pos"][0] + 0.5 and point[0] >= player["pos"][0] - 0.5 and point[1] > player["pos"][1]:
                collisions.append([point[0], player["pos"][1]])
        
        yInt = [point[0], int(point[1])]
        
        while True:
            if world[int(yInt[0])][yInt[1] - 1]["type"] != 0 or yInt[1] <= 0:
                collisions.append(yInt)
                break
            else:
                yInt[1] -= 1
    
    # If the ray is pointing straight down, this performs a simplified version of the calculations that don't screw around with xInt.
    elif slope == "-inf":
        for player in players:
            if player["team"] == team:
                continue
            
            elif point[0] <= player["pos"][0] + 0.5 and point[0] >= player["pos"][0] - 0.5 and point[1] < player["pos"][1]:
                collisions.append([point[0], player["pos"][1]])
        
        yInt = [point[0], int(point[1]) + 1]
        
        while True:
            if yInt[1] >= worldSize[1]:
                collisions.append(yInt)
                break
            elif world[int(yInt[0])][yInt[1]]["type"] != 0:
                collisions.append(yInt)
                break
            else:
                yInt[1] += 1
    
    #If the slope isn't undefined or 0 (99% of the time), this calculates collisions.
    else:
        
        b1 = point[1] - (slope * point[0])# Useful thing, it's the y-intercept of the ray.
        
        #Calculates collisions with players
        for player in players:
            if player["team"] == team:
                continue
            
            #All of the following is based on a bunch of really annoying algebra.
            m2 = -1 / (slope) # Slope of a line that is perpendicular to the ray.
            b2 = player["pos"][1] - (m2 * player["pos"][0]) # y-intercept of a line that is perpendicular to the ray, and passes through the center of a player.
            xCoord = (b2 - b1) / (slope - m2) # x position of the intersection between y=m2 + b2 and y=slope + b1
            yCoord = slope * xCoord + b1 # y position of the intersection between y=m2 + b2 and y=slope + b1
            
            # Checks if the intersection between the lines is within the player's body.
            if math.sqrt(math.pow(xCoord - player["pos"][0], 2) + math.pow(yCoord - player["pos"][1], 2)) <= 0.5:
                
                # Makes sure that the intersection is on the correct side of the entire fucking universe.
                if dir < 0 and point[0] > xCoord:
                    collisions.append([xCoord, yCoord])
                    
                elif dir > 0 and point[0] < xCoord:
                    collisions.append([xCoord, yCoord])
        
        # everything is pain
        # Sets up a bunch of stuff.
        # I didn't even understand how this works when I made it.
        if slope > 0:
            if dir > 0:
                stepX = 1
                stepY = 1
                xInt = [int(point[0]) + 1, slope * (int(point[0]) + 1) + b1]
                yInt = [(((int(point[1]) + 1) - point[1]) / slope) + point[0], int(point[1]) + 1]
                offSetX = 0
                offSetY = 0
                
            else:
                stepX = -1
                stepY = -1
                xInt = [int(point[0]), slope * (int(point[0])) + b1]
                yInt = [(((int(point[1])) - point[1]) / slope) + point[0], int(point[1])]
                offSetX = -1
                offSetY = -1
                
        else:
            if dir > 0:
                stepX = 1
                stepY = -1
                xInt = [int(point[0]) + 1, slope * (int(point[0]) + 1) + b1]
                yInt = [(((int(point[1])) - point[1]) / slope) + point[0], int(point[1])]
                offSetX = 0
                offSetY = -1
                
            else:
                stepX = -1
                stepY = 1
                xInt = [int(point[0]), slope * (int(point[0])) + b1]
                yInt = [(((int(point[1]) + 1) - point[1]) / slope) + point[0], int(point[1]) + 1]
                offSetX = -1
                offSetY = 0
        
        # This loops through the world, checking for collisions with blocks.
        while True:
            
            # Checks if xInt is closer to 'point' than yInt.
            # If it is, this does the math for checking if xInt is a collision.
            if math.sqrt(math.pow(point[0] - xInt[0], 2) + math.pow(point[1] - xInt[1], 2)) <= math.sqrt(math.pow(point[0] - yInt[0], 2) + math.pow(point[1] - yInt[1], 2)):
                
                # Checks if xInt is outside the world, and exits the loop if it is.
                if xInt[0] >= worldSize[0] or xInt[1] >= worldSize[1] or xInt[0] <= 0 or xInt[1] <= 0:
                    collisions.append(xInt)
                    break
                
                else:
                    # This checks if xInt is intersecting with a block in the world.
                    if world[int(xInt[0]) + offSetX][int(xInt[1])]["type"] != 0:
                        collisions.append(xInt)
                        break
                    
                    else:
                        # If xInt is neither outside the world nor a block in the world, where ever it just was is assumed to be air and the loop continues on.
                        xInt = [xInt[0] + stepX, xInt[1] + slope * stepX]
            
            #If xInt is not closer than yInt, this determines if yInt is a collision.
            else:
                # Checks if yInt is outside the world, and exits the loop if it is.
                if yInt[0] >= worldSize[0] or yInt[1] >= worldSize[1] or yInt[0] <= 0 or yInt[1] <= 0:
                    collisions.append(yInt)
                    break
                
                else:
                    # This checks if yInt is intersecting with a block in the world.
                    if world[int(yInt[0])][int(yInt[1]) + offSetY]["type"] != 0:
                        collisions.append(yInt)
                        break
                    
                    else:
                        # If yInt is neither outside the world nor a block in the world, where ever it just was is assumed to be air and the loop continues on.
                        yInt = [yInt[0] + 1 / (slope * stepY), yInt[1] + stepY]
            
            
    ### PICKS CLOSEST COLLISION ###
                        
    # If there are no collisions, this assumes that the ray went off the world but was not detected.
    # Calculates and returns the intersection of the ray with the edge of the world.
    if collisions == []:
        
        # If the ray is straight up, do a really simple calculation.
        if slope == "+inf":
            return [point[0], 0.0]
        
        # If the ray is straight down, do a really simple calculation.
        elif slope == "-inf":
            return [point[0], worldSize[1]]
        
        # If the ray is horizontal, do another simple calculation.
        elif slope == 0:
            if dir < 0:
                return [0.0, point[1]]
            
            else:
                return [worldSize[1], point[1]]
        
        # Otherwise, do stuff with math. 
        else:
            if dir < 0:
                return [0.0, point[1] - (slope * point[0])] # This mess is derived from the point-slope equation for a line.
            
            else:
                return [worldSize[0], (worldSize[0] * slope) + (point[1] - (slope * point[0]))] # This mess is also derived from the point-slope equation for a line.
    
    #If there are collisions that happened, this finds which one is closest.
    else:
        nearestCollision = collisions[0]
        
        # Loops through 'collisions' and finds the nearest one.
        for i in range(len(collisions)):
            
            # Checks if the next collision in the list is closer than the current nearest collision.
            if math.sqrt(math.pow(collisions[i][0] - point[0], 2) + math.pow(collisions[i][1] - point[1], 2)) < math.sqrt(math.pow(nearestCollision[0] - point[0], 2) + math.pow(nearestCollision[1] - point[1], 2)):
                nearestCollision = collisions[i]
        
        return nearestCollision
    

# This takes a slope and a direction (similar to 'raycast') and returns an angle in degrees.
# which makes server communication slightly less painful.
# (when it eventually exists)
def toDeg(rotation):
    if rotation[1] == 0:
        if rotation[0] == "+inf":
            return 90.0
        
        else:
            return 270.0
        
    elif rotation[1] > 0:
        if rotation[0] > 0:
            return math.atan(rotation[0]) * (180 / math.pi)
        
        else:
            return (math.atan(rotation[0]) * (180 / math.pi)) + 360
        
    elif rotation[1] < 0:
        return math.atan(rotation[0]) * (180 / math.pi) + 180

# This takes an angle in degrees and returns a slope/direction list.
def toSlope(deg):
    if deg == 90.0:
        return ["+inf", 1]
    
    elif deg == 270.0:
        return ["-inf", 1]
    
    elif deg < 90:
        return [math.tan(deg * (math.pi / 180)), 1]
    
    elif deg > 90 and deg < 270:
        return [math.tan((deg - 180) * (math.pi / 180)), -1]
    
    else:
        return [math.tan((deg - 360) * (math.pi / 180)), 1]
    

# Mildly important.
def main():
    
    ### DISPLAY VARIABLES ###################################################################################
    
    ### DETERMINES IF DEBUG TOOLS SHOULD BE ENABLED ###
    
    global worldSize
        
    worldSize = [0, 0]
    
    global world
        
    world = []
    
    while True:
        displayPlayerInfo = input("Enable debug tools? (y/n): ")
        
        if displayPlayerInfo.lower() == "y":
            displayPlayerInfo = True
            break
        
        elif displayPlayerInfo.lower() == "n":
            displayPlayerInfo = False
            break
    
    while True:
        fromFile = input("Import world from file? (y/n): ")
        
        if fromFile.lower() == "y":
            fromFile = True
            break
        
        elif fromFile.lower() == "n":
            fromFile = False
            break
    
    if fromFile:
        
        worldImport = open(os.path.join("data", "world", "world.txt"), "r") # Imports the world from a file, and stores its' lines in 'rawWorld'
        rawWorld = worldImport.readlines()
        worldImport.close()
        del worldImport
        
        for line in range(len(rawWorld)):
            rawWorld[line] = rawWorld[line].strip()
            if line == 0:
                continue
            elif len(rawWorld[line]) != len(rawWorld[line - 1]):
                pygame.quit()
                raise IndexError("Width of the world MUST be consistent")

        # The following two loops rotate the array, so to refer to a block position in the world you can write world[x][y] rather that world[y][x]
        for i in range(len(rawWorld[0])):
            world.append([])

        for x in range(len(world)):
            for y in range(len(rawWorld)):
                world[x].append({"type":int(rawWorld[y][x])})

        # Converts each int in 'world' to an item in a list, so it can be easily modified.
        for line in range(len(world)):
            world[line] = list(world[line])

        del rawWorld # boop
        
        worldSize = [len(world), len(world[0])] # Size of the world
    
    else:
        
        
        while True:
            worldSize[0] = input("Width of the world (int): ")
            
            if worldSize[0].isdigit():
                worldSize[0] = int(worldSize[0])
                break
        
        while True:
            worldSize[1] = input("Height of the world (int): ")
            
            if worldSize[1].isdigit():
                worldSize[1] = int(worldSize[1])
                break
        
        
        
        for x in range(worldSize[0]):
            world.append([])
            for y in range(worldSize[1]):
                world[x].append({"type":0})
    
    
    global scrW
    
    scrW = pygame.display.Info().current_w # Width of the screen
    
    global scrH
    
    scrH = pygame.display.Info().current_h # Height of the screen

    window = pygame.display.set_mode((scrW, scrH), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF) # The screen
    
    pygame.display.set_caption("BaseRace")
    
    colors = {"orange":[255, 128, 0], "blue":[0, 128, 255], "white":[255, 255, 255], "black":[0, 0, 0], "dark blue":[0, 64, 128], "dark orange":[128, 64, 0], "green":[0, 255, 0], "grey":[223, 223, 223]} # Dictionary of colors
    
    fpsDisplayFont = pygame.font.Font(os.path.join("data", "fonts", "desc.ttf"), int(scrH / 50)) # Font to display the fps with. Delete this if you're removing the fps counter.
    
    monoFont = pygame.font.Font(os.path.join("data", "fonts", "VT323-Regular.ttf"), int(scrH * (25 / 540))) # Another font.
    
    lastFrameTime = time.time() # Used to determine if the screen should update, because there's no point in rendering graphics at 800hz if your monitor only supports 60hz.
    
    statusBarDims = [scrW / 10, scrH / 20]

    healthBarPos = [scrW * (25 / 1920), scrH * (19 / 20) - scrH * (104 / 1080)]
    
    energyBarPos = [scrW * (25 / 1920), scrH * (19 / 20) - scrH * (25 / 1080)]
    
    ### CAMERA VARIABLES ###################################################################################
    
    global cameraPos
    
    cameraPos = [16.0, 16.0] # Position of the camera
    
    global cameraZoom
    
    cameraZoom = 16 # Number of blocks that can fit in the width of the screen
    
    previousZoom = 16 # DO NOT TOUCH DURING THE MAIN LOOP. Used to determine if sprites should be resized.
    
    ### PLAYER VARIABLES ###################################################################################
    
    teams = [{"color":colors["blue"]}, {"color":colors["orange"]}] # Player teams. Currently only contains information on team color.
    
    global players
    
    players = [{"team":0, "health":100, "pos":[16.0, 16.0], "energy":100, "rotation":[0, 0], "isShooting":False}, {"team":0, "health":100, "pos":[12.0, 4.0], "energy":100, "rotation":[-0.5, 1], "isShooting":False}, {"team":1, "health":100, "pos":[18.0, 29.0], "energy":100, "rotation":[5.1, 1], "isShooting":False}, {"team":1, "health":100, "pos":[18.0, 27.0], "energy":100, "rotation":[2.3, -1], "isShooting":True}]
    
    cornerCollideFlag = False
    
    global playerRadius
    
    playerRadius = int(scrW / (2 * cameraZoom)) # Radius of the player's body
    
    playerDelta = [0.0, 0.0] # Vectors to change the player's position by.
    
    playerSpeed = 0.01
    
    relPlayerPos = [scrW // 2, scrH // 2] # Relative position of the player on the screen, in pixels.
    
    playerLaserDist = int((3 * scrW) / (8 * cameraZoom)) # Distance from the center of the player's body to the center of the darker-colored circle that shows where they're facing.
    
    inputSet = [0, 0, 0, 0, 0, 0] # Used to record keystrokes of directional input and mouse input. The order is [W, S, A, D, LCLICK, RCLICK]. 1 = being pushed and 0 = not being pushed.
    
    ### WORLD VARIABLES ###################################################################################
    
    blocks = [] # List of block types. These will be defined in a loop.

    blockSprites = []
    
    startTime = time.time() # Unix time that the game was started.

    gameExit = False # Determines if the game should exit. False for running, True for exiting.
    
    t = pygame.time.Clock() # A clock for doing clock-related things, like getting FPS.
    
    #########################################################################################################################################################################################
    ### INITIALIZATION ######################################################################################################################################################################
    #########################################################################################################################################################################################
    
    ### FILLS OUT THE "BLOCKS" LIST WITH COLORED SURFACES, WHOSE INDEX CORRESPONDS TO BLOCK ID'S ###

    blockSprites = []
    
    for block in range(3):
        blocks.append(pygame.Surface([scrW / cameraZoom, scrW / cameraZoom]).convert())

    blocks[0].fill(colors["grey"])
    blocks[0].fill(colors["white"], pygame.Rect([(scrW / cameraZoom) / 40, (scrW / cameraZoom) / 40], [(scrW / cameraZoom) - (scrW / cameraZoom) / 20, (scrW / cameraZoom) - (scrW / cameraZoom) / 20]))
    blocks[1].fill(colors["black"])
    blocks[2].fill(colors["orange"])

    for sprite in blocks:
        blockSprites.append(sprite.copy())

    # Placeholder block ID list:
    # 0 - Air
    # 1 - Black wall
    # 2 - Orange wall
    

    
    #########################################################################################################################################################################################
    ### MAIN LOOP ###########################################################################################################################################################################
    #########################################################################################################################################################################################

    while not gameExit:
        t.tick() # Ticks the clock. As of version 0.0.wheneverTazwelBitchedAtMeToPutMoreCommentsInMyCode, this is only used for displaying FPS.
        mousePos = pygame.mouse.get_pos() # Gets mouse position.
        
        #Event handler, gets & handles input.
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                
                # This sets corresponding directional keys in 'inputSet' to 1 if they're being pushed.
                if event.key == K_ESCAPE:
                    gameExit = True
                    
                elif event.key == K_d:
                    inputSet[3] = 1
                    
                elif event.key == K_a:
                    inputSet[2] = 1
                    
                elif event.key == K_w:
                    inputSet[0] = 1
                    
                elif event.key == K_s:
                    inputSet[1] = 1
                
                #Debug tools, they zoom the camera out or in:
                elif event.key == K_e:
                    cameraZoom = 60.5
                    
                elif event.key == K_f:
                    cameraZoom = 16
                    
            elif event.type == KEYUP:
                
                # This sets corresponding directional keys in 'inputSet' to 0 if they're not being pushed.
                if event.key == K_d:
                    inputSet[3] = 0
                    
                elif event.key == K_a:
                    inputSet[2] = 0
                    
                elif event.key == K_w:
                    inputSet[0] = 0
                    
                elif event.key == K_s:
                    inputSet[1] = 0
                    
            elif event.type == MOUSEBUTTONDOWN:
                
                # This sets corresponding mouse buttons in 'inputSet' to 1 if they're being pushed.
                if event.button == 1: # Left click detection
                    inputSet[4] = 1
                    
                elif event.button == 3: # Right click detection
                    inputSet[5] = 1

            elif event.type == MOUSEBUTTONUP:
                # This sets corresponding mouse buttons in 'inputSet' to 0 if they're not being pushed.
                if event.button == 1: # Left click detection
                    inputSet[4] = 0
                    
                elif event.button == 3: # Right click detection
                    inputSet[5] = 0
        
        # Checks if the mouse is being clicked, and makes the player start shooting if it is.
        if inputSet[4] == 1:
            players[0]["isShooting"] = True
            
        else:
            players[0]["isShooting"] = False
        
        # Based on what keys are being pressed (WSAD, or the first four values in inputSet, respectively),
        # this changes playerDelta.
        if (inputSet[0] != inputSet[1]) and (inputSet[2] != inputSet[3]): # This checks if up OR down, and left OR right are being pressed, to see if the player should be moved diagonally.
            if inputSet[0] == 1: # This checks if up is being pressed.
                
                if inputSet[2] == 1: # This checks if left is being pressed
                    playerDelta = [math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2) * (-1), math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2) * (-1)] # Move the player diagonally up and left.
                    
                else: # Because we already know that left is NOT being pressed at this point, and that up IS being pressed, we already know to move the player up and right.
                    playerDelta = [math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2), math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2) * (-1)] # Move the player diagonally up and right.
                    
            else: #If down is NOT being pressed:
                
                if inputSet[2] == 1: # Check if right is being pressed
                    playerDelta = [math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2) * (-1), math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2)] # Move the player diagonally down and left.
                    
                else: # The only possible other option is down and left being pressed.
                    playerDelta = [math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2), math.sqrt(math.pow((t.get_time() * playerSpeed), 2) / 2)] # Move the player diagonally down and right.
                    
        else: # If the player is NOT pressing diagonally:
            
            if inputSet[0] == 1 or inputSet[1] == 1: # Check if the player is pressing up or down
                
                if inputSet[0] == inputSet[1]: # If the player is pressing up AND down, the inputs cancel out and the player does not move.
                    playerDelta[1] = 0 # Don't move the player vertically.
                    
                elif inputSet[0] == 1: # Check if the player is ONLY pressing up
                    playerDelta[1] =  -(t.get_time() * playerSpeed) # Move the player vertically up. This is negative because of the grid system being dumb.
                    
                else: # If up OR down are being pressed, and down is NOT being pressed, we know to move the player vertically down
                    playerDelta[1] = (t.get_time() * playerSpeed) # Move the player vertically down. This is positive because of the grid system being dumb.
                    
            else: # If neither up nor down are being pressed, don't move the player vertically.
                playerDelta[1] = 0 # Don't move the player vertically.
                
            if inputSet[2] == 1 or inputSet[3] == 1: # Check if the player is pressing left or right
                
                if inputSet[2] == inputSet[3]: # If the player is pressing left AND right, the inputs cancel out and the player does not move.
                    playerDelta[0] = 0 # Don't move the player horizontally.
                    
                elif inputSet[2] == 1: # Check if the player is ONLY pressing left
                    playerDelta[0] =  -(t.get_time() * playerSpeed) # Move the player horizontally left.
                    
                else: # If left OR right are being pressed, and left is NOT being pressed, we know to move the player horizontally right.
                    playerDelta[0] = (t.get_time() * playerSpeed) # Move the player horizontally right.
                    
            else: # If neither left NOR right are being pressed, don't move the player vertically.
                playerDelta[0] = 0 # Don't move the player horizontally.
                
                
        
        # Makes sure the player does not go outside the world by checking if incrementing the player's position by
        # playerDelta would put it outside of the world.
        # Rather than just setting playerDelta to 0, it makes it so the player *perfectly* squishes up against the side of the world,
        # so we can maintain delicious pixel-perfectness
        if playerDelta[0] + players[0]["pos"][0] < 0.5: # Check if the player will go outside the right edge
            playerDelta[0] = -(players[0]["pos"][0] - 0.5) # Place the player perfectly 0.5 grid-base units next to the edge of the world.
            
        elif playerDelta[0] + players[0]["pos"][0] > worldSize[0] - 0.5: # Check if the player will go outside the left edge
            playerDelta[0] = (worldSize[0] - 0.5) - players[0]["pos"][0] # Place the player perfectly 0.5 grid-base units next to the edge of the world.
        
        if playerDelta[1] + players[0]["pos"][1] > worldSize[1] - 0.5: # Check if the player will go outside the bottom edge
            playerDelta[1] = (worldSize[1] - 0.5) - players[0]["pos"][1] # Place the player perfectly 0.5 grid-base units next to the edge of the world.
            
        elif playerDelta[1] + players[0]["pos"][1] < 0.5: # Check if the player will go outside the top edge
            playerDelta[1] = -(players[0]["pos"][1] - 0.5) # Place the player perfectly 0.5 grid-base units next to the edge of the world.
        
        ### COLLISIONS ###
        
        preArcPos = [0, 0]
        nextPlayerPos = [players[0]["pos"][0] + playerDelta[0], players[0]["pos"][1] + playerDelta[1]]
        pointPos = [int(nextPlayerPos[0] + 0.5), int(nextPlayerPos[1] + 0.5)]
        collideRange = [[int(nextPlayerPos[0] + 0.5), int(nextPlayerPos[1] + 0.5)], [int(nextPlayerPos[0] + 0.5), int(nextPlayerPos[1] - 0.5)], [int(nextPlayerPos[0] - 0.5), int(nextPlayerPos[1] + 0.5)], [int(nextPlayerPos[0] - 0.5), int(nextPlayerPos[1] - 0.5)]]
        magnitude = math.sqrt(math.pow(playerDelta[0], 2) + math.pow(playerDelta[1], 2))
        
        
        for block in enumerate(collideRange):
            if block[1][0] < 0 or block[1][0] >= worldSize[0]:
                collideRange[block[0]] = "EOW"
            if block[1][1] < 0 or block[1][1] >= worldSize[1]:
                collideRange[block[0]] = "EOW"
        
        
        for block in collideRange:
            if block == "EOW":
                continue
            
            if world[block[0]][block[1]]["type"] != 0:
                
                if math.sqrt(math.pow(nextPlayerPos[0] - pointPos[0], 2) + math.pow(nextPlayerPos[1] - pointPos[1], 2)) < 0.45:
                    #math.sqrt(math.pow(playerDeta[0], 2) + math.pow(playerDeta[1], 2))
                    
                    if (nextPlayerPos[0] - pointPos[0]) != 0:
                        if block == [int(nextPlayerPos[0] + 0.5), int(nextPlayerPos[1] + 0.5)]:
                            collideAngle = math.atan(((nextPlayerPos[1] - pointPos[1])) / ((nextPlayerPos[0] - pointPos[0])))
                            playerDelta = [-(magnitude * math.cos(-collideAngle)), (magnitude * math.sin(-collideAngle))]
                            
                        if block == [int(nextPlayerPos[0] + 0.5), int(nextPlayerPos[1] - 0.5)]:
                            collideAngle = math.atan((nextPlayerPos[1] - pointPos[1]) / ((nextPlayerPos[0] - pointPos[0])))
                            playerDelta = [-(magnitude * math.cos(-collideAngle)), (magnitude * math.sin(-collideAngle))]

                        if block == [int(nextPlayerPos[0] - 0.5), int(nextPlayerPos[1] + 0.5)]:
                            collideAngle = math.atan((nextPlayerPos[1] - pointPos[1]) / (nextPlayerPos[0] - pointPos[0])) ##
                            playerDelta = [(magnitude * math.cos(collideAngle)), magnitude * math.sin(collideAngle)]
                        
                        if block == [int(nextPlayerPos[0] - 0.5), int(nextPlayerPos[1] - 0.5)]:
                            collideAngle = math.atan((nextPlayerPos[1] - pointPos[1]) / (nextPlayerPos[0] - pointPos[0])) ##
                            playerDelta = [(magnitude * math.cos(collideAngle)), magnitude * math.sin(collideAngle)]
                    

                        
                    
                
                
                if players[0]["pos"][0] >= block[0] - 0.05 and players[0]["pos"][0] <= block[0] + 1.05:
                    if block[1] - players[0]["pos"][1] <= 0:
                        playerDelta[1] = block[1] - (players[0]["pos"][1] + 0.5) + 2
                    else:
                        playerDelta[1] = block[1] - (players[0]["pos"][1] + 0.5)
                
                if players[0]["pos"][1] >= block[1] - 0.05 and players[0]["pos"][1] <= block[1] + 1.05:
                    if block[0] - players[0]["pos"][0] <= 0:
                        playerDelta[0] = block[0] - (players[0]["pos"][0] + 0.5) + 2
                    else:
                        playerDelta[0] = block[0] - (players[0]["pos"][0] + 0.5)
                
                    
                        
        # Changes player position by playerDelta
        players[0]["pos"] = [players[0]["pos"][0] + playerDelta[0], players[0]["pos"][1] + playerDelta[1]]
        
        # Changes camera position, with smoothness.
        # Also allows the player to look around with the mouse.
        cameraPos = [cameraPos[0] + ((((mousePos[0] - (scrW / 2)) / (scrW / cameraZoom)) / 200) + (players[0]["pos"][0] - cameraPos[0]) / 50) * (t.get_time() * 0.5), cameraPos[1] + ((((mousePos[1] - (scrH / 2)) / (scrW / cameraZoom)) / 200) + (players[0]["pos"][1] - cameraPos[1]) / 50) * (t.get_time() * 0.5)] 
        

        # Determines if sprites should be resized.
        if cameraZoom != previousZoom: # Checks if the camera zoom is different
        
            playerLaserDist = int((3 * scrW) / (8 * cameraZoom)) # Scales the distance from the player's laser to the player
            
            if cameraZoom == 16: # This is for maintaining pixel-perfectness for when the camera is at default zoom.
                
                # Loops through the block sprites and resizes them to a perfect whole-number side-length for 1920x1080
                for sprite in range(len(blocks)):
                    blockSprites[sprite] = blocks[sprite].copy()
                # Note that if this were written in any other programming language on Earth, this would be a
                # huge and disgusting memory leak, because the previous sprites aren't actually deleted.
                
            else: # If the camera is no longer in the default zoom, (for quick camera pans and zoom-outs), don't bother with integer division
                
                #Same thing as the other loop, it just doesn't bother with integer division and rounds up to the nearest pixel.
                for sprite in range(len(blocks)):
                    blockSprites[sprite] = pygame.transform.scale(blocks[sprite].copy(), [int(scrW / cameraZoom) + 1, int(scrW / cameraZoom) + 1])
                    
        
        # If you screw with the following line, all of the sprites will be resized every single frame even if they don't have to be.
        
        #///CAUTION///CAUTION///CAUTION///CAUTION
        previousZoom = cameraZoom# DO NOT TOUCH
        #///CAUTION///CAUTION///CAUTION///CAUTION
        
        
        
        #This makes it so the camera does not go outside the world when it isn't zoomed out very far
        if cameraZoom <= worldSize[0]: # Check if the number of blocks that can fit in the width of the screen is less than the width of the world
            
            if cameraPos[0] - (cameraZoom / 2) < 0: # Check if the camera is outside the left edge of the world
                cameraPos[0] = cameraZoom / 2 # Move the camera back into the world if the above is true.
                
            elif cameraPos[0] + (cameraZoom / 2) > worldSize[0]: # Check if the camera is outside the right edge of the world
                cameraPos[0] = worldSize[0] - (cameraZoom / 2) # Move the camera back into the world if the above is true.
            
            if cameraPos[1] < (cameraZoom * (scrH / scrW)) / 2: # Check if the camera is outside the top edge of the world
                cameraPos[1] = (cameraZoom * (scrH / scrW)) / 2 # Move the camera back into the world if the above is true.
                
            elif cameraPos[1] > worldSize[1] - (cameraZoom * (scrH / scrW)) / 2: # Check if the camera is outside the bottom edge of the world
                cameraPos[1] = worldSize[1] - (cameraZoom * (scrH / scrW)) / 2 # Move the camera back into the world if the above is true.
                
        else: # If the camera DOES exceed the world size, meaning restricting it to the world is impossible:
            window.fill(colors["white"]) # Fill the screen with white (or whatever we decide to make the color of air in the future), so there aren't weird graphical artifacts.

            
        # This the important thing.
        # It renders the section of the world that's visible to the camera.
        # It only does so when ~1/120th of a second has passed.
        if time.time() - lastFrameTime > 0.008:
            for column in range(int(cameraPos[0] - (cameraZoom / 2)) - 1, int(cameraPos[0] + (cameraZoom / 2)) + 1): # Scans accross the world area of the world visible to the camera in columns
                if column < 0 or column > worldSize[0] - 1: # If the column is outside of the world, continue, because that would crash the program.
                    continue
                else:
                    for row in range(int(cameraPos[1] - ((cameraZoom * (scrH / scrW)) // 2)) - 1, int(cameraPos[1] + ((cameraZoom * (scrH / scrW)) // 2)) + 2): # Scans accross the world area of the world visible to the camera in rows
                        
                        if row < 0 or row >= worldSize[1]: # If the row is outside of the world, continue, because that would crash the program.
                            continue
                        
                        else:
                            window.blit(blockSprites[world[column][row]["type"]], [(column - cameraPos[0] + (cameraZoom / 2)) * (scrW / cameraZoom), (row - cameraPos[1] + (cameraZoom * (scrH / scrW)) / 2) * (scrW / cameraZoom)]) # Blit the corresponding sprite to the block type in the column and row in the relative position of the block on the screen.
                            # If the above line, or anything in this loop breaks, make it so I'm the one to fix it.
                            # I don't want to subject this shitshow to anyone else.
                        
##                        if [column, row] in collideRange:
##                            window.blit(blockSprites[2], [(column - cameraPos[0] + (cameraZoom / 2)) * (scrW / cameraZoom), (row - cameraPos[1] + (cameraZoom * (scrH / scrW)) / 2) * (scrW / cameraZoom)])
                            
                            
                            ########## Uncomment the following line to display block positions (terrible performance): ##########
                            #window.blit(fpsDisplayFont.render("(" + str(column) + ", " + str(row) + ")", 0, (255, 0, 0)), [(column - cameraPos[0] + (cameraZoom // 2)) * (scrW / cameraZoom), (row - cameraPos[1] + (cameraZoom * (scrH / scrW)) // 2) * (scrW / cameraZoom) + (scrW / (cameraZoom * 2))])
            
            # Displays the player's lasers, if they're firing
            for player in players:
                if player["isShooting"]:
                    if player["energy"] - (time.time() - lastFrameTime) * 30 > 0:
                        pygame.draw.line(window, teams[player["team"]]["color"], getScreenPos(player["pos"]), getScreenPos(raycast(player["pos"], player["rotation"][0], player["rotation"][1], player["team"])), 4)
                        
                        if player["energy"] - (time.time() - lastFrameTime) * 30 > 0:
                            player["energy"] = player["energy"] - (time.time() - lastFrameTime) * 30
                        else:
                            player["energy"] = 0
                
                if player["energy"] < 100 and player["energy"] + (time.time() - lastFrameTime) * 15 < 100:
                    player["energy"] += (time.time() - lastFrameTime) * 15
                    
                elif player["energy"] < 100:
                    player["energy"] = 100
                    
            
            
            # Displays players.
            for player in players:
                relPlayerPos = getScreenPos(player["pos"]) # Gets the relative position of the player on the screen
                
                
                # This block is what displays players.
                if players.index(player) == 0:
                    # Calculates the player's rotation.
                    if mousePos[0] - relPlayerPos[0] > 0: # Checks if the mouse is on the right side of the screen
                        player["rotation"] = [(relPlayerPos[1] - mousePos[1]) / (relPlayerPos[0] - mousePos[0]), 1]
                        
                    elif mousePos[0] - relPlayerPos[0] < 0: # Checks if the mouse is on the left side of the screen
                        player["rotation"] = [(relPlayerPos[1] - mousePos[1]) / (relPlayerPos[0] - mousePos[0]), -1]
                    
                    elif mousePos[1] > relPlayerPos[1]:
                        player["rotation"] = ["-inf", 0]
                    
                    else:
                        player["rotation"] = ["+inf", 0]
                
                
                # Draws the player's body.
                pygame.draw.circle(window, teams[player["team"]]["color"], relPlayerPos, int(scrW / (2 * cameraZoom)), 0)
                
                # Draws the player's adorable little cicle that shows where they're facing.
                # Checks if the player's rotation isn't straight up or down.
                if str(type(player["rotation"][0])) == "<class 'float'>" or str(type(player["rotation"][0])) == "<class 'int'>":
                    pygame.draw.circle(window, [teams[player["team"]]["color"][0] // 2, teams[player["team"]]["color"][1] // 2, teams[player["team"]]["color"][2] // 2], [int(math.cos(math.atan(player["rotation"][0])) * playerLaserDist) * player["rotation"][1] + relPlayerPos[0], int(math.sin(math.atan(player["rotation"][0])) * playerLaserDist) * player["rotation"][1] + relPlayerPos[1]], int(scrW / (8 * cameraZoom)), 0) # Blits the circle.
                
                # Catches if the player's rotation is straight up.
                elif player["rotation"][0] == "+inf":
                    pygame.draw.circle(window, [teams[player["team"]]["color"][0] // 2, teams[player["team"]]["color"][1] // 2, teams[player["team"]]["color"][2] // 2], [relPlayerPos[0], relPlayerPos[1] - playerLaserDist], int(scrW / (8 * cameraZoom)), 0) # Blits the circle.
                
                # Catches if the player's rotation is straight down.
                else:
                    pygame.draw.circle(window, [teams[player["team"]]["color"][0] // 2, teams[player["team"]]["color"][1] // 2, teams[player["team"]]["color"][2] // 2], [relPlayerPos[0], relPlayerPos[1] + playerLaserDist], int(scrW / (8 * cameraZoom)), 0) # Blits the circle.
                
                # If debug tools are enabled, this displays player information.
                if displayPlayerInfo:
                    for attribute in enumerate(player):
                        window.blit(fpsDisplayFont.render(str(attribute[1]) + ": " + str(player[attribute[1]]), 0, (255, 0, 0)), [relPlayerPos[0] + scrW / 32, relPlayerPos[1] + attribute[0] * 30])
            
            ### EVERYTHING PAST THIS POINT IS UI ###
            
            #pygame.draw.circle(window, [255, 0, 0], getScreenPos(pointPos), 5)
            
            # Draws health and energy bar borders.
            pygame.draw.rect(window, [32, 255, 64], pygame.Rect(healthBarPos, statusBarDims), 2)
            pygame.draw.rect(window, [64, 128, 255], pygame.Rect(energyBarPos, statusBarDims), 2)
            
            # Draws health and energy bar interiors.
            window.fill([32, 255, 64], pygame.Rect(healthBarPos, [statusBarDims[0] * (players[0]["health"] / 100), statusBarDims[1]]))
            window.fill([64, 128, 255], pygame.Rect(energyBarPos, [statusBarDims[0] * (players[0]["energy"] / 100), statusBarDims[1]]))
            
            # Draws text over health and energy bars.
            window.blit(monoFont.render("HEALTH", 0, (32, 128, 16)), healthBarPos)
            window.blit(monoFont.render("ENERGY", 0, (16, 64, 128)), energyBarPos)
                
            # Framerate counter. Delete these at will.
            # (but if you're going to, get rid of 'fpsDisplayFont')
            fps = t.get_fps()
            window.blit(fpsDisplayFont.render("fps: " + str(fps), 0, (255, 0, 0)), [0, 0])
        
            #Updates the screen
            lastFrameTime = time.time()
            pygame.display.flip()

    pygame.quit()

main()

