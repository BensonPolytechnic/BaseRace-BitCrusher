def cutscene(startPos, endPos, startZoom, endZoom, panDuration, pause):
    global cameraPos
    
    global cameraZoom
    
    global playerLaserDist
    
    startTime = time.time()
    
    endTime = startTime + panDuration
    
    previousZoom = 16
    
    lastFrameTime = time.time()
    
    healthSprite = pygame.Surface([scrW / cameraZoom, scrW / cameraZoom]).convert_alpha()
    
    healthSprite.fill([0, 0, 0, 64])

    while time.time() < endTime + pause:
        if time.time() < endTime:
            cameraPos = [(endPos[0] - startPos[0]) * (math.cos(math.pi * (((time.time() - startTime) / panDuration) + 1)) + 1) / 2 + startPos[0], (endPos[1] - startPos[1]) * (math.cos(math.pi * (((time.time() - startTime) / panDuration) + 1)) + 1) / 2 + startPos[1]]
            cameraZoom = (endZoom - startZoom) * (math.cos(math.pi * (((time.time() - startTime) / panDuration) + 1)) + 1) / 2 + startZoom
        else:
            cameraPos = endPos
            cameraZoom = endZoom
    
        if cameraZoom != previousZoom: # Checks if the camera zoom is different
            playerLaserDist = int((3 * scrW) / (8 * cameraZoom)) # Scales the distance from the player's laser to the player
            
            
            if cameraZoom == 16: # This is for maintaining pixel-perfectness for when the camera is at default zoom.
                
                healthSprite = pygame.Surface([scrW / cameraZoom, scrW / cameraZoom]).convert_alpha()
                healthSprite.fill([0, 0, 0, 64])
                
                # Loops through the block sprites and resizes them to a perfect whole-number side-length for 1920x1080
                for block in range(len(blockSprites)):
                    for state in range(len(blockSprites[block])):
                        for rotation in range(len(blockSprites[block][state])):
                            blockSprites[block][state][rotation] = blockData[block]["sprites"][state][rotation].copy()
                # Note that if this were written in any other programming language on Earth, this would be a
                # huge and disgusting memory leak, because the previous sprites aren't actually deleted.
                
            else: # If the camera is no longer in the default zoom, (for quick camera pans and zoom-outs), don't bother with integer division
                
                #Same thing as the other loop, it just doesn't bother with integer division and rounds up to the nearest pixel.
                
                healthSprite = pygame.Surface([int(scrW / cameraZoom) + 1, int(scrW / cameraZoom) + 1]).convert_alpha()
                healthSprite.fill([0, 0, 0, 64])
                
                for block in range(len(blockSprites)):
                    for state in range(len(blockSprites[block])):
                        for rotation in range(len(blockSprites[block][state])):
                            blockSprites[block][state][rotation] = pygame.transform.scale(blockData[block]["sprites"][state][rotation].copy(), [int(scrW / cameraZoom) + 1, int(scrW / cameraZoom) + 1])
        
        # If you screw with the following line, all of the sprites will be resized every single frame even if they don't have to be.
        
        #///CAUTION///CAUTION///CAUTION///CAUTION
        previousZoom = cameraZoom# DO NOT TOUCH
        #///CAUTION///CAUTION///CAUTION///CAUTION
        
        
        window.fill([255, 255, 255]) # Fill the screen with white (or whatever we decide to make the color of air in the future), so there aren't weird graphical artifacts.

            
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
                         # Blit the corresponding sprite to the block type in the column and row in the relative position of the block on the screen.
                            window.blit(blockSprites[world[column][row]["type"]][world[column][row]["state"]][world[column][row]["rotation"]], [(column - cameraPos[0] + (cameraZoom / 2)) * (scrW / cameraZoom), (row - cameraPos[1] + (cameraZoom * (scrH / scrW)) / 2) * (scrW / cameraZoom)])
                            
                            if world[column][row]["type"] != 0 and world[column][row]["health"] / blockData[world[column][row]["type"]]["health"] != 1:
                                healthSprite.fill([0, 0, 0, 64])
                                healthSprite.fill([0, 0, 0, 0], pygame.Rect([(healthSprite.get_width() / 2) * (1 - world[column][row]["health"] / blockData[world[column][row]["type"]]["health"]), (healthSprite.get_width() / 2) * (1 - world[column][row]["health"] / blockData[world[column][row]["type"]]["health"])], [healthSprite.get_width() * (world[column][row]["health"] / blockData[world[column][row]["type"]]["health"]), healthSprite.get_width() * (world[column][row]["health"] / blockData[world[column][row]["type"]]["health"])]))
                                window.blit(healthSprite, getScreenPos([column, row]))
                                
            
            # Displays the player's lasers, if they're firing
            for player in players:
                
                relPlayerPos = getScreenPos(player["pos"]) # Gets the relative position of the player on the screen
                
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

            
            #Updates the screen
            lastFrameTime = time.time()
            
            pygame.display.flip()