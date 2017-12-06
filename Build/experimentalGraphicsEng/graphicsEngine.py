# *** GRAPHICS ENGINE ***
# This is a thing that makes pixels on a screen turn pretty colors

import pygame, os, time, math
from pygame.locals import *

pygame.init()

#This takes a point, a slope ("+inf" for straight up and "-inf" for straight down), and a direction (-1 for towards -x, 1 for toward x, and 0 for neither) and returns the nearest intersection of that ray with a block in the world.
#Does not work yet.
def raycast(point, slope, dir=0):
    return slope

def main():
    startTime = time.clock()

    scrW = pygame.display.Info().current_w
    scrH = pygame.display.Info().current_h
    colors = {"orange":[255, 128, 0], "blue":[0, 128, 255], "white":[255, 255, 255], "black":[0, 0, 0], "dark blue":[0, 64, 128], "dark orange":[128, 64, 0]} # Dictionary of colors
    
    window = pygame.display.set_mode((scrW, scrH), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    cameraPos = [16.0, 16.0] # Position of the camera
    cameraZoom = 16 # Number of blocks that can fit in the width of the screen
    previousZoom = 16 # DO NOT TOUCH DURING THE MAIN LOOP. Used to determine if sprites should be resized.
    playerLaserDist = int((3 * scrW) / (4 * cameraZoom)) # Distance from the center of the player to the center of the small circle that shows where they're facing.

    #Makes a list of block types. We'll probably import these from a file in the future.
    blocks = []

    for block in range(3):
        blocks.append(pygame.Surface([scrW / cameraZoom, scrW / cameraZoom]).convert())
    blocks[0].fill(colors["white"])
    blocks[1].fill(colors["black"])
    blocks[2].fill(colors["orange"])

    """
    Placeholder block ID list:

    0 - Air
    1 - Black wall
    2 - Orange wall
    """

    playerRadius = int(scrW / (2 * cameraZoom)) # Radius of the player's body
    playerPos = [16.0, 16.0] # Position of the player
    playerDelta = [0.0, 0.0] # Vectors to change the player's position by.
    relPlayerPos = [scrW // 2, scrH // 2] # Position of the player on the screen
    playerLaserDist = int((3 * scrW) / (8 * cameraZoom))

    #Imports the world from a file. In later versions, this won't be necessary.
    global world # this is global so it can be accessed in the raycast() function
    world = []
    worldImport = open(os.path.join("data", "world", "world.txt"), "r")
    rawWorld = worldImport.readlines()
    worldImport.close()
    del worldImport

    # Checks to make sure each line in the world has the same number of characters
    for line in range(len(rawWorld)):
        rawWorld[line] = rawWorld[line].strip()
        if line == 0:
            continue
        elif len(rawWorld[line]) != len(rawWorld[line - 1]):
            pygame.quit()
            raise IndexError("Width of the world MUST be consistent")

    # The following two loops rotate the rawWorld array so that if you want to reference a block, so you can say world[x][y], rather than world[y][x]
    # (this will also be gotten rid of when we do this for real)
    for i in range(len(rawWorld[0])):
        world.append([])

    for x in range(len(world)):
        for y in range(len(rawWorld)):
            world[x].append(int(rawWorld[y][x]))

    #Converts each string in 'world' to an item in a list, so it can be easily modified.
    for line in range(len(world)):
        world[line] = list(world[line])

    del rawWorld

    worldSize = [len(world), len(world[0])] # Size of the world
    t = pygame.time.Clock() # A clock for doing clock-related things

    fpsDisplayFont = pygame.font.Font(os.path.join("data", "fonts", "desc.ttf"), int(scrH / 50)) # Font to display the fps with. Delete this if you're removing the fps counter.

    inputSet = [0, 0, 0, 0, 0, 0] # Used to record keystrokes of directional input and mouse input. The order is [W, S, A, D, LCLICK, RCLICK]. 1 = being pushed and 0 = not being pushed.

    gameExit = False

    while not gameExit:
        t.tick()
        mousePos = pygame.mouse.get_pos()
        
        #Event handler, gets input
        for event in pygame.event.get():
            if event.type == KEYDOWN:
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
                if event.key == K_d:
                    inputSet[3] = 0
                elif event.key == K_a:
                    inputSet[2] = 0
                elif event.key == K_w:
                    inputSet[0] = 0
                elif event.key == K_s:
                    inputSet[1] = 0
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    inputSet[4] = 1
                elif event.button == 3:
                    inputSet[5] = 1
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    inputSet[4] = 0
                elif event.button == 3:
                    inputSet[5] = 0
        
        #Processes input from the left, right, up, and down keys. Turns it into a number to change the player position by based on the amount of time since the last frame.
        
        if (inputSet[0] != inputSet[1]) and (inputSet[2] != inputSet[3]): # Stupid fucking python not having a stupid fucking XOR operator.
            if inputSet[0] == 1: # Stupid fucking python not having a stupid fucking XOR operator.
                if inputSet[2] == 1: # Stupid fucking python not having a stupid fucking XOR operator.
                    playerDelta = [math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2) * (-1), math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2) * (-1)] # Stupid fucking python not having a stupid fucking XOR operator.
                else: # Stupid fucking python not having a stupid fucking XOR operator.
                    playerDelta = [math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2), math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2) * (-1)] # Stupid fucking python not having a stupid fucking XOR operator.
            else: # Stupid fucking python not having a stupid fucking XOR operator.
                if inputSet[2] == 1: # Stupid fucking python not having a stupid fucking XOR operator.
                    playerDelta = [math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2) * (-1), math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2)] # Stupid fucking python not having a stupid fucking XOR operator.
                else: # Stupid fucking python not having a stupid fucking XOR operator.
                    playerDelta = [math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2), math.sqrt(math.pow((t.get_time() * 0.01), 2) / 2)] # Stupid fucking python not having a stupid fucking XOR operator.
        else:
            if inputSet[0] == 1 or inputSet[1] == 1:
                if inputSet[0] == inputSet[1]:
                    playerDelta[1] = 0
                elif inputSet[0] == 1:
                    playerDelta[1] =  -(t.get_time() * 0.01)
                else:
                    playerDelta[1] = (t.get_time() * 0.01)
            else:
                playerDelta[1] = 0
                
            if inputSet[2] == 1 or inputSet[3] == 1:
                if inputSet[2] == inputSet[3]:
                    playerDelta[0] = 0
                elif inputSet[2] == 1:
                    playerDelta[0] =  -(t.get_time() * 0.01)
                else:
                    playerDelta[0] = (t.get_time() * 0.01)
            else:
                playerDelta[0] = 0
        
        #The following 2 If/Elif statements make sure the player doesn't go outside the world
        if playerDelta[0] + playerPos[0] < 0.5:
            playerDelta[0] = -(playerPos[0] - 0.5) # mether hecking pixel perfectness
        elif playerDelta[0] + playerPos[0] > worldSize[0] - 0.5: #splitting them up like this is actually better for performance.
            playerDelta[0] = (worldSize[0] - 0.5) - playerPos[0]
        
        if playerDelta[1] + playerPos[1] > worldSize[1] - 0.5:
            playerDelta[1] = (worldSize[1] - 0.5) - playerPos[1]
        elif playerDelta[1] + playerPos[1] < 0.5:
            playerDelta[1] = -(playerPos[1] - 0.5)
        
        playerPos = [playerPos[0] + playerDelta[0], playerPos[1] + playerDelta[1]] # Changes player position
        cameraPos = [cameraPos[0] + (playerPos[0] - cameraPos[0]) / 100, cameraPos[1] + (playerPos[1] - cameraPos[1]) / 100] # Changes camera position, with delicious smoothness.
        
    #     PLACE ALL CHANGES TO THE CAMERA POSITION ABOVE THIS POINT ||
    #                                                               ||
    #     Because if the camera ends up even slightly outside       ||
    #     of the world it will freak out and crash.                 ||
    #   (this is the part that actually blits stuff)                \/
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if cameraZoom != previousZoom:
            playerLaserDist = int((3 * scrW) / (8 * cameraZoom))
            if cameraZoom == 16:
                for block in range(len(blocks)):
                    blocks[block] = pygame.transform.scale(blocks[block], [scrW // 16, scrW // 16])
            else:
                for block in range(len(blocks)):
                    blocks[block] = pygame.transform.scale(blocks[block], [int(scrW / cameraZoom) + 1, int(scrW / cameraZoom) + 1])
                
        previousZoom = cameraZoom
        

        window.fill(colors["white"])
        
        for column in range(int(cameraPos[0] - (cameraZoom / 2)) - 2, int(cameraPos[0] + (cameraZoom / 2)) + 2):
            if column < 0 or column > worldSize[0] - 1:
                continue
            else:
                for row in range(int(cameraPos[1] - ((cameraZoom * (scrH / scrW)) // 2)) - 2, int(cameraPos[1] + ((cameraZoom * (scrH / scrW)) // 2)) + 3):
                    if row < 0 or row > worldSize[1] - 1:
                        continue
                    elif world[column][row] == 0:
                        continue
                    else:
                        window.blit(blocks[world[column][row]], [(column - cameraPos[0] + (cameraZoom / 2)) * (scrW / cameraZoom), (row - cameraPos[1] + (cameraZoom * (scrH / scrW)) / 2) * (scrW / cameraZoom)])
                        
                        # Uncomment the following line to display block positions (terrible performance):
                        #window.blit(fpsDisplayFont.render("(" + str(column) + ", " + str(row) + ")", 0, (255, 0, 0)), [(column - cameraPos[0] + (cameraZoom // 2)) * (scrW / cameraZoom), (row - cameraPos[1] + (cameraZoom * (scrH / scrW)) // 2) * (scrW / cameraZoom) + (scrW / (cameraZoom * 2))])
        
        relPlayerPos = [int((playerPos[0] - cameraPos[0] + (cameraZoom / 2)) * ((scrW / cameraZoom))), int((playerPos[1] - cameraPos[1] + (cameraZoom * (scrH / scrW)) / 2) * (scrW / cameraZoom))] # Relative player position on the screen.
        pygame.draw.circle(window, colors["blue"], relPlayerPos, int(scrW / (2 * cameraZoom)), 0) #Blits the player to the screen.
        
        #I don't even know
        if mousePos[0] - relPlayerPos[0] > 0:
            relAngle = math.atan((mousePos[1] - relPlayerPos[1]) / (mousePos[0] - relPlayerPos[0]))
            pygame.draw.circle(window, colors["dark blue"], [int(math.cos(relAngle) * playerLaserDist) + relPlayerPos[0], int(math.sin(relAngle) * playerLaserDist) + relPlayerPos[1]], int(scrW / (8 * cameraZoom)), 0)
        elif mousePos[0] - relPlayerPos[0] < 0:
            relAngle = math.atan((mousePos[1] - relPlayerPos[1]) / (mousePos[0] - relPlayerPos[0]))
            pygame.draw.circle(window, colors["dark blue"], [int(math.cos(relAngle) * playerLaserDist) * -1 + relPlayerPos[0], int(math.sin(relAngle) * playerLaserDist) * -1 + relPlayerPos[1]], int(scrW / (8 * cameraZoom)), 0)
        else:
            if mousePos[1] - relPlayerPos[1] > 0:
                relAngle = "+inf"
                pygame.draw.circle(window, colors["dark blue"], [relPlayerPos[0], playerLaserDist + relPlayerPos[1]], int(scrW / (8 * cameraZoom)), 0)
            else:
                relAngle = "-inf"
                pygame.draw.circle(window, colors["dark blue"], [relPlayerPos[0], playerLaserDist - relPlayerPos[1]], int(scrW / (8 * cameraZoom)), 0)
        
        # This is what will draw the laser
        if inputSet[4] == 1:
            if mousePos[0] == relPlayerPos[0]:
                if mousePos[1] > relPlayerPos[1]:
                    ray = raycast(playerPos, "+inf")
                else:
                    ray = raycast(playerPos, "-inf")
            else:
                ray = raycast(playerPos, (relPlayerPos[1] - mousePos[1]) / (relPlayerPos[0] - mousePos[0]) * (-1), (relPlayerPos[0] - mousePos[0]))
            
            window.blit(fpsDisplayFont.render(str(ray), 0, (255, 0, 0)), [scrW / 2, scrH / 3])
            #pygame.draw.line(window, colors["blue"], relPlayerPos, raycast(), 5)

        # pygame.draw.circle(window, colors["orange"], [scrW // 2, scrH // 2], int(scrW / (2 * cameraZoom)), 0)
        fps = t.get_fps()
        window.blit(fpsDisplayFont.render(str(fps), 0, (255, 0, 0)), [0, 0])
        
        pygame.display.flip()

    pygame.quit()

main()