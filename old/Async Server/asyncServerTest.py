import time, socket, threading, select, queue

def handleConnections(dataQueue):
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = "127.0.0.1"
    
    port = 8888
    
    srvSocket.bind((host, port))
    
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
                    sock.send(data)
                    
                    

def main():
    dataQueue = queue.Queue(128)
    
    clientData = []
    
    threadLocker = threading.Lock()
    
    connectionHandler = threading.Thread(target=handleConnections, args=(dataQueue,))
    
    connectionHandler.start()
    
    serverRunning = True
    
    while serverRunning:
        
        for item in range(dataQueue.qsize()):
            clientData.append(dataQueue.get())
            
        for item in clientData:
            clientData.remove(item)
        
        
        
        # Do stuff
    

main()