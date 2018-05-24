import time, socket, threading, select, queue, os, math

def hitscan(point, slope, dir=0, team=None):

    # If the slope is 0, this performs a simplified version of the calculations that don't screw around with yInt.
    if slope == 0:

        # Detects collisions with players.
        # Only checks for collisions with the players on the other team.
        for player in players:
            if player["team"] == team:
                continue

            elif point[1] <= player["pos"][1] + 0.5 and point[1] >= player["pos"][1] - 0.5:
                return player

    # If the ray is pointing straight up, this performs a simplified version of the calculations that don't screw around with xInt.
    elif slope == "+inf":

        # Detects collisions with players.
        # Only checks for collisions with the players on the other team.
        for player in players:
            if player["team"] == team:
                continue

            elif point[0] <= player["pos"][0] + 0.5 and point[0] >= player["pos"][0] - 0.5 and point[1] > player["pos"][1]:
                return player

    # If the ray is pointing straight down, this performs a simplified version of the calculations that don't screw around with xInt.
    elif slope == "-inf":
        for player in players:
            if player["team"] == team:
                continue

            elif point[0] <= player["pos"][0] + 0.5 and point[0] >= player["pos"][0] - 0.5 and point[1] < player["pos"][1]:
                return player

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
                    return player

                elif dir > 0 and point[0] < xCoord:
                    return player

    return None

def raycast(point, slope, dir=0, team=None):
    collisions = []

    # If the slope is 0, this performs a simplified version of the calculations that don't screw around with yInt.
    if slope == 0:
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
                return None



            elif blockData[world[xInt[0] + offSetX][int(xInt[1])]["type"]]["collidable"] or xInt[0] >= worldSize[0] + offSetX or xInt[0] <= 0:
                return [xInt[0] + offSetX, int(xInt[1])]



            else:
                xInt[0] += stepX

    # If the ray is pointing straight up, this performs a simplified version of the calculations that don't screw around with xInt.
    elif slope == "+inf":


        yInt = [point[0], int(point[1])]

        while True:
            if blockData[world[int(yInt[0])][yInt[1] - 1]["type"]]["collidable"] or yInt[1] <= 0:
                return [int(yInt[0]), yInt[1] - 1]



            else:
                yInt[1] -= 1

    # If the ray is pointing straight down, this performs a simplified version of the calculations that don't screw around with xInt.
    elif slope == "-inf":

        yInt = [point[0], int(point[1]) + 1]

        while True:
            if yInt[1] >= worldSize[1]:
                return None

            elif blockData[world[int(yInt[0])][yInt[1]]["type"]]["collidable"]:
                return [int(yInt[0]), yInt[1]]

            else:
                yInt[1] += 1

    #If the slope isn't undefined or 0 (99% of the time), this calculates collisions.
    else:

        b1 = point[1] - (slope * point[0])# Useful thing, it's the y-intercept of the ray.

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
                    return None

                else:
                    # This checks if xInt is intersecting with a block in the world.
                    if blockData[world[int(xInt[0]) + offSetX][int(xInt[1])]["type"]]["collidable"]:
                        return [int(xInt[0]) + offSetX, int(xInt[1])]

                    else:
                        # If xInt is neither outside the world nor a block in the world, where ever it just was is assumed to be air and the loop continues on.
                        xInt = [xInt[0] + stepX, xInt[1] + slope * stepX]

            #If xInt is not closer than yInt, this determines if yInt is a collision.
            else:
                # Checks if yInt is outside the world, and exits the loop if it is.
                if yInt[0] >= worldSize[0] or yInt[1] >= worldSize[1] or yInt[0] <= 0 or yInt[1] <= 0:
                    return None

                else:
                    # This checks if yInt is intersecting with a block in the world.
                    if blockData[world[int(yInt[0])][int(yInt[1]) + offSetY]["type"]]["collidable"]:
                        return [int(yInt[0]), int(yInt[1]) + offSetY]


                    else:
                        # If yInt is neither outside the world nor a block in the world, where ever it just was is assumed to be air and the loop continues on.
                        yInt = [yInt[0] + 1 / (slope * stepY), yInt[1] + stepY]



def handleConnections(sendQueue, dataQueue, port):
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    srvSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

    #host = "127.0.0.1"

    host = ""

    srvSocket.bind((host, port))

    srvSocket.listen(4)

    sendData = []

    cData = None

    descriptors = [srvSocket]

    while True:

        # Await an event on a readable socket descriptor
        (sread, swrite, sexc) = select.select(descriptors, [], [])

        for sock in sread:

            # Received a connect to the server (listening) socket
            if sock == srvSocket:
                descriptors.append(sock.accept()[0])
                print("Got client")

            else:
                try:
                    data = sock.recv(1024)
                except:
                    continue

                if data == '':
                    sock.close()
                    descriptors.remove(sock)

                else:
                    dataQueue.put(data.decode('ascii'))

        for item in range(sendQueue.qsize()):
            cData = sendQueue.get()
            sendQueue.task_done()
            sendData.append(cData)

        for sock in descriptors:
            for item in range(len(sendData)):
                if sock != srvSocket:
                    try:
                        sock.send(sendData[item])
                    except:
                        continue

        sendData = []

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

def complicatePlayerArray(simpleArray):
    playerArray = {}

    for player in range(len(simpleArray)):

        playerArray["team"] = int(simpleArray[0])

        playerArray["health"] = int(simpleArray[4])

        playerArray["pos"] = [int(simpleArray[1]) / 100, int(simpleArray[2]) / 100]

        playerArray["energy"] = int(simpleArray[5])

        playerArray["rotation"] = toSlope(float(simpleArray[3]))

        playerArray["isShooting"] = bool(int(simpleArray[6]))

        playerArray["delta"] = [float(simpleArray[7]), float(simpleArray[8])]

    return playerArray

def simplePlayer(player):
    simpleArray = []

    for i in range(9):
        simpleArray.append("0")

    for key in player:
        if key == "team":
            simpleArray[0] = str(player["team"])

        elif key == "pos":
            simpleArray[1] = str(int(player["pos"][0] * 100))
            simpleArray[2] = str(int(player["pos"][1] * 100))

        elif key == "rotation":
            simpleArray[3] = str(toDeg(player["rotation"]))

        elif key == "health":
            simpleArray[4] = str(int(player["health"]))

        elif key == "energy":
            simpleArray[5] = str(int(player["energy"]))

        elif key == "isShooting":

            if player["isShooting"]:
                simpleArray[6] = "1"
            else:
                simpleArray[6] = "0"

        elif key == "delta":
            simpleArray[7] = str(player["delta"][0])
            simpleArray[8] = str(player["delta"][1])

    return ",".join(simpleArray)

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

def importBlockData():
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

def getDistance(pointA, pointB):
    return math.sqrt(math.pow(pointA[0] - pointB[0], 2) + math.pow(pointA[1] - pointB[1], 2))

def main():
    while True:
        port = input("Port of the server: ")

        if port.isdigit():
            port = int(port)
            break

    dataQueue = queue.Queue(128)

    sendQueue = queue.Queue(128)

    clientData = []

    connectionHandler = threading.Thread(target=handleConnections, args=(sendQueue, dataQueue, port))

    connectionHandler.start()

    serverRunning = True

    global blockData
    blockData = importBlockData()

    global worldSize
    worldSize = [32, 64]

    global world
    world = []

    for x in range(worldSize[0]):
        world.append([])

        for y in range(worldSize[1]):
            world[x].append({"type":0, "state":0, "rotation":0, "health":0})


    playerUpdates = []

    uniquePlayers = []

    blockUpdates = []

    wireUpdates = []

    playerInUpdates = False

    serverComFrequency = 30

    wires = []

    lastComTime = time.time()

    offloadedWires = []

    offloadedBlocks = []

    offloadedPlayers = []

    blockCollision = None

    playerCollision = None

    global players

    players = [{"team":0, "health":100, "pos":[14.0, 16.0], "energy":100, "rotation":[0.0, 1], "isShooting":False, "delta":[0.0, 0.0]},
     {"team":0, "health":100, "pos":[18.0, 16.0], "energy":100, "rotation":[0.0, 1], "isShooting":False, "delta":[0.0, 0.0]},
      {"team":1, "health":100, "pos":[14.0, 48.0], "energy":100, "rotation":[0.0, 1], "isShooting":False, "delta":[0.0, 0.0]},
       {"team":1, "health":100, "pos":[18.0, 48.0], "energy":100, "rotation":[0.0, 1], "isShooting":False, "delta":[0.0, 0.0]}]


    while serverRunning:
        for item in range(dataQueue.qsize()):
            clientData.append(dataQueue.get())
            dataQueue.task_done()

        if clientData != []:
            for packet in clientData:
                packet = packet.split("|")

                for item in packet:
                    if item == '':
                        continue
                    elif item[0] == "0":
                        playerUpdates.append(item)

                    elif item[0] == "1":
                        blockUpdates.append(item)

                    elif item[0] == "2":
                        wireUpdates.append(item)

            clientData = []


        if time.time() - lastComTime >= 1 / serverComFrequency:
            lastComTime = time.time()

            if blockUpdates != []:
                for update in blockUpdates:
                    if update == '':
                        blockUpdates.remove(update)

                for update in range(len(blockUpdates)):
                    blockUpdates[update] = blockUpdates[update][2:]

                offloadedBlocks = blockUpdates

                for block in offloadedBlocks:
                    if block == "":
                        continue

                    block = block.split(",")

                    if len(block) < 7:
                        break

                    for char in block:
                        if char == '':
                            block.remove(char)

                    try:
                        world[int(block[0])][int(block[1])] = {"type":int(block[2]), "state":int(block[3]), "rotation":int(block[4]), "health":int(block[5]), "special":block[6]}
                    except:
                        print(block)

                offloadedBlocks = []

                blockUpdates = "*".join(blockUpdates)

                blockUpdates = "|1," + blockUpdates + "|"

                sendQueue.put(bytes(blockUpdates, "ascii"))

                blockUpdates = []

            if wireUpdates != []:
                for update in wireUpdates:
                    if update == '':
                        wireUpdates.remove(update)

                for update in range(len(wireUpdates)):
                    wireUpdates[update] = wireUpdates[update][2:]

                offloadedWires = wireUpdates

                for wire in offloadedWires:
                    if wire == "":
                        continue

                    wire = wire.split(",")

                    if len(wire) < 6:
                        break

                    if wire[0] == "0":
                        #Wire removal
                        wires.remove([[int(wire[1]), int(wire[2])], [int(wire[3]), int(wire[4]), int(wire[5])]])

                    elif wire[0] == "1":
                        print("wire added")
                        wires.append([[int(wire[1]), int(wire[2])], [int(wire[3]), int(wire[4]), int(wire[5])]])

                offloadedWires = []

                wireUpdates = "*".join(wireUpdates)

                wireUpdates = "|2," + wireUpdates + "|"

                sendQueue.put(bytes(wireUpdates, "ascii"))

                wireUpdates = []

            if playerUpdates != []:
                for update in playerUpdates:
                    update = update[2:]
                    update = update.split(",")

                    if update == []:
                        continue

                    if uniquePlayers == []:
                        update.pop(0)
                        uniquePlayers.append(update)
                    else:
                        playerInUpdates = False

                        for player in uniquePlayers:
                            if player[1] == update[1]:
                                if float(player[0]) < float(update[0]):
                                    playerInUpdates = True
                                    break


                        if not playerInUpdates:
                            update.pop(0)
                            uniquePlayers.append(update)

                playerUpdates = []

                if uniquePlayers != []:
                    for update in range(len(uniquePlayers)):
                        uniquePlayers[update] = ",".join(uniquePlayers[update])

                    offloadPlayers = uniquePlayers

                    for player in offloadPlayers:
                        if player == "":
                            continue

                        player = player.split(",")

                        if len(player) < 7:
                            break

                        players[int(player[0])] = complicatePlayerArray(player[1:])


                    offloadPlayers = []


                    uniquePlayers = "*".join(uniquePlayers)

                    uniquePlayers = "|0," + uniquePlayers + "|"

                    sendQueue.put(bytes(uniquePlayers, "ascii"))

                    uniquePlayers = []

            for wire in wires:
                if not (blockData[world[wire[1][0]][wire[1][1]]["type"]]["wireable"] or blockData[world[wire[0][0]][wire[0][1]]["type"]]["wireable"]):
                    wires.remove(wire)
                    print("removing wire")
                    continue


                elif world[wire[1][0]][wire[1][1]]["type"] == 4:
                    if wire[1][2] == 0:
                        world[wire[1][0]][wire[1][1]]["special"] = str(int(world[wire[0][0]][wire[0][1]]["state"])) + world[wire[1][0]][wire[1][1]]["special"][1]

                    elif wire[1][2] == 1:
                        world[wire[1][0]][wire[1][1]]["special"] = world[wire[1][0]][wire[1][1]]["special"][0] + str(int(world[wire[0][0]][wire[0][1]]["state"]))

                    if world[wire[1][0]][wire[1][1]]["special"] == "11":
                        if world[wire[1][0]][wire[1][1]]["state"] != 1:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",1," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," + str(world[wire[1][0]][wire[1][1]]["health"])+ "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                    else:
                        if world[wire[1][0]][wire[1][1]]["state"] != 0:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",0," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," +  str(world[wire[1][0]][wire[1][1]]["health"])+ "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                elif world[wire[1][0]][wire[1][1]]["type"] == 5:
                    if wire[1][2] == 0:
                        world[wire[1][0]][wire[1][1]]["special"] = str(int(world[wire[0][0]][wire[0][1]]["state"])) + world[wire[1][0]][wire[1][1]]["special"][1]

                    elif wire[1][2] == 1:
                        world[wire[1][0]][wire[1][1]]["special"] = world[wire[1][0]][wire[1][1]]["special"][0] + str(int(world[wire[0][0]][wire[0][1]]["state"]))

                    if world[wire[1][0]][wire[1][1]]["special"] != "00":
                        if world[wire[1][0]][wire[1][1]]["state"] != 1:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",1," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," + str(world[wire[1][0]][wire[1][1]]["health"])+ "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                    else:
                        if world[wire[1][0]][wire[1][1]]["state"] != 0:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",0," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," +  str(world[wire[1][0]][wire[1][1]]["health"])+ "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                elif world[wire[1][0]][wire[1][1]]["type"] == 6:
                    if wire[1][2] == 0:
                        world[wire[1][0]][wire[1][1]]["special"] = str(int(world[wire[0][0]][wire[0][1]]["state"])) + world[wire[1][0]][wire[1][1]]["special"][1]

                    elif wire[1][2] == 1:
                        world[wire[1][0]][wire[1][1]]["special"] = world[wire[1][0]][wire[1][1]]["special"][0] + str(int(world[wire[0][0]][wire[0][1]]["state"]))

                    if world[wire[1][0]][wire[1][1]]["special"] == "01" or world[wire[1][0]][wire[1][1]]["special"] == "10":
                        if world[wire[1][0]][wire[1][1]]["state"] != 1:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",1," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," + str(world[wire[1][0]][wire[1][1]]["health"]) + "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                    else:
                        if world[wire[1][0]][wire[1][1]]["state"] != 0:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",0," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," + str(world[wire[1][0]][wire[1][1]]["health"]) + "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                elif world[wire[1][0]][wire[1][1]]["type"] == 7:
                    if wire[1][2] == 0:
                        world[wire[1][0]][wire[1][1]]["special"] = str(int(world[wire[0][0]][wire[0][1]]["state"])) + world[wire[1][0]][wire[1][1]]["special"][1]

                    if world[wire[1][0]][wire[1][1]]["special"] == "10":
                        if world[wire[1][0]][wire[1][1]]["state"] != 1:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",1," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," + str(world[wire[1][0]][wire[1][1]]["health"]) + "," + str(world[wire[1][0]][wire[1][1]]["special"]))

                    else:
                        if world[wire[1][0]][wire[1][1]]["state"] != 0:
                            blockUpdates.append("1," + str(wire[1][0]) + "," + str(wire[1][1]) + "," + str(world[wire[1][0]][wire[1][1]]["type"]) + ",0," + str(world[wire[1][0]][wire[1][1]]["rotation"]) + "," + str(world[wire[1][0]][wire[1][1]]["health"]) + "," + str(world[wire[1][0]][wire[1][1]]["special"]))

            for player in range(len(players)):
                if players[player]["isShooting"]:
                    blockCollision = raycast(players[player]["pos"], players[player]["rotation"][0], players[player]["rotation"][1], players[player]["team"])
                    playerCollision = hitscan(players[player]["pos"], players[player]["rotation"][0], players[player]["rotation"][1], players[player]["team"])

                    if playerCollision == None and blockCollision == None:
                        continue

                    elif playerCollision == None and blockCollision != None:
                        if world[blockCollision[0]][blockCollision[1]]["health"] - 50 <= 0:
                            blockUpdates.append("1," + str(blockCollision[0]) + "," + str(blockCollision[1]) + "," + "0,0,0,0,00")
                        else:
                            blockUpdates.append("1," + str(blockCollision[0]) + "," + str(blockCollision[1]) + "," + str(world[blockCollision[0]][blockCollision[1]]["type"]) + "," + str(world[blockCollision[0]][blockCollision[1]]["state"]) + "," + str(world[blockCollision[0]][blockCollision[1]]["rotation"]) + "," + str(world[blockCollision[0]][blockCollision[1]]["health"] - 50) + "," + str(world[blockCollision[0]][blockCollision[1]]["special"]))

                    elif playerCollision != None and blockCollision != None:
                        if getDistance(players[player]["pos"], blockCollision) <= getDistance(players[player]["pos"], playerCollision["pos"]):
                            if world[blockCollision[0]][blockCollision[1]]["health"] - 50 <= 0:
                                blockUpdates.append("1," + str(blockCollision[0]) + "," + str(blockCollision[1]) + "," + "0,0,0,0,00")
                            else:
                                blockUpdates.append("1," + str(blockCollision[0]) + "," + str(blockCollision[1]) + "," + str(world[blockCollision[0]][blockCollision[1]]["type"]) + "," + str(world[blockCollision[0]][blockCollision[1]]["state"]) + "," + str(world[blockCollision[0]][blockCollision[1]]["rotation"]) + "," + str(world[blockCollision[0]][blockCollision[1]]["health"] - 50) + "," + str(world[blockCollision[0]][blockCollision[1]]["special"]))

        # Do stuff


main()
