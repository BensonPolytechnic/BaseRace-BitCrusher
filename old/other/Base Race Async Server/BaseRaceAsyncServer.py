import time, socket, threading, select, queue, os

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
                        print("o shit")
                        continue

        sendData = []

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
    worldSize = [64, 128]

    global world
    world = []

    for x in range(worldSize[0]):
        world.append([])

        for y in range(worldSize[1]):
            world[x].append({"type":0, "state":0, "rotation":0, "health":0})


    playerUpdates = []

    uniquePlayers = []

    blockUpdates = []

    playerInUpdates = False

    serverComFrequency = 120

    lastComtime = time.time()

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

        if time.time() - lastComtime >= 1 / serverComFrequency:
            lastComTime = time.time()

            if blockUpdates != []:
                for update in blockUpdates:
                    if update == '':
                        blockUpdates.remove(update)

                for update in range(len(blockUpdates)):
                    blockUpdates[update] = blockUpdates[update][2:]

                blockUpdates = "*".join(blockUpdates)

                blockUpdates = "|1," + blockUpdates + "|"

                sendQueue.put(bytes(blockUpdates, "ascii"))

                blockUpdates = []

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

                    uniquePlayers = "*".join(uniquePlayers)

                    uniquePlayers = "|0," + uniquePlayers + "|"

                    sendQueue.put(bytes(uniquePlayers, "ascii"))

                    uniquePlayers = []





        ########## AT VERY BOTTOM FOR THE LOVE OF FUCK
        clientData = []


        # Do stuff


main()
