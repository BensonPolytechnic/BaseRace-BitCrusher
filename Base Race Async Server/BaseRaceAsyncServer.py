import time, socket, threading, select, queue

def handleConnections(dataQueue, port):
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #host = "127.0.0.1"
    
    host = ""
    
    srvSocket.bind((host, port))
    
    print("Address: " + str(srvSocket.getsockname()))
    
    srvSocket.listen(4)
    
    descriptors = [srvSocket]
    
    while True:
     
        # Await an event on a readable socket descriptor
        (sread, swrite, sexc) = select.select(descriptors, [], [])
     
        
        for sock in sread:

            # Received a connect to the server (listening) socket
            if sock == srvSocket:
                descriptors.append(sock.accept()[0])
                
            else:
                data = sock.recv(1024)
                
                if data == '':
                    sock.close()
                    descriptors.remove(sock)
                    
                else:
                    dataQueue.put(data.decode('ascii'))

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

            elif blockData[world[xInt[0] + offSetX][int(xInt[1])]["type"]]["collidable"] or xInt[0] >= worldSize[0] + offSetX or xInt[0] <= 0:
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
            if blockData[world[int(yInt[0])][yInt[1] - 1]["type"]]["collidable"] or yInt[1] <= 0:
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

            elif blockData[world[int(yInt[0])][yInt[1]]["type"]]["collidable"]:
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
                    if blockData[world[int(xInt[0]) + offSetX][int(xInt[1])]["type"]]["collidable"]:
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
                    if blockData[world[int(yInt[0])][int(yInt[1]) + offSetY]["type"]]["collidable"]:
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

def importBlockData(pixels):
    blockInfo = [] # Stores lines of 'blockdata.txt'

    blockInfoImport = open(os.path.join("data", "blocks", "blockdata.txt"), "r") # File object used to import data

    blockFileData = blockInfoImport.readlines() # Reads the lines

    # Deletes the file object because it isn't needed anymore.
    blockInfoImport.close()

    del blockInfoImport

    blockLine = 0 # Value used for incrementing through sets of block data

    # Strips whitespace off of file data
    for line in range(len(blockFileData)):
        blockFileData[line] = blockFileData[line].strip()

    # pain is all
    for line in range(len(blockFileData)):
        if blockFileData[line] == "{":
            blockInfo.append({})

            blockLine = 0

            while True:
                if blockFileData[line + blockLine] == "}":
                    break

                elif blockFileData[line + blockLine][:blockFileData[line+blockLine].find(".")] == "int":
                    blockInfo[len(blockInfo) - 1][blockFileData[line + blockLine][blockFileData[line + blockLine].find(".") + 1:blockFileData[line + blockLine].find(":")]] = int(blockFileData[line + blockLine][blockFileData[line + blockLine].find(":") + 1:blockFileData[line + blockLine].find(";")])

                elif blockFileData[line + blockLine][:blockFileData[line+blockLine].find(".")] == "bool":
                    blockInfo[len(blockInfo) - 1][blockFileData[line + blockLine][blockFileData[line + blockLine].find(".") + 1:blockFileData[line + blockLine].find(":")]] = bool(int(blockFileData[line + blockLine][blockFileData[line + blockLine].find(":") + 1:blockFileData[line + blockLine].find(";")]))

                elif blockFileData[line + blockLine][:blockFileData[line+blockLine].find(".")] == "str":
                    blockInfo[len(blockInfo) - 1][blockFileData[line + blockLine][blockFileData[line + blockLine].find(".") + 1:blockFileData[line + blockLine].find(":")]] = blockFileData[line + blockLine][blockFileData[line + blockLine].find(":") + 1:blockFileData[line + blockLine].find(";")]

                elif blockFileData[line + blockLine][:blockFileData[line+blockLine].find(".")] == "float":
                    blockInfo[len(blockInfo) - 1][blockFileData[line + blockLine][blockFileData[line + blockLine].find(".") + 1:blockFileData[line + blockLine].find(":")]] = float(blockFileData[line + blockLine][blockFileData[line + blockLine].find(":") + 1:blockFileData[line + blockLine].find(";")])

                blockLine += 1 # bebebebebebebebebe

    return blockInfo # eeeeeeeeeeeeee

def main():
    while True:
        port = input("Port of the server: ")
        
        if port.isdigit():
            port = int(port)
            break
    
    dataQueue = queue.Queue(128)
    
    clientData = []
    
    connectionHandler = threading.Thread(target=handleConnections, args=(dataQueue, port))
    
    connectionHandler.start()
    
    serverRunning = True
    
    clientData = []
    
    global blockData
    blockData = importBlockData()
    
    global worldSize
    worldSize = [64, 128]
    
    global world
    world = []
    
    for x in range(worldSize[0]):
        world.append([])

        for y in range(worldSize[1]):
            world[x].append({"type":0, "state":0, "rotation":0, "health":0})
    
    while serverRunning:
        
        for item in range(dataQueue.qsize()):
            clientData.append(dataQueue.get())
        
        if clientData != []:
            clientData = clientData.join()
            
            if client
            
        
        
        
        
        # Do stuff
    

main()