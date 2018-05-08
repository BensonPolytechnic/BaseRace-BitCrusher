import socket, time, math, multiprocessing
def main():
    queue = []
    
    #creates a socket that uses regular IP and TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #lets the user specify the IP of the server, 127.0.0.1 for testing
    port = 8888
    #Connects on the last two variables
    s.bind(('127.0.0.1', port))
    
    s.listen(5)
    
   # Establish connection with client.
    c, addr = s.accept()
    print ('Got connection from', addr)
 
   # send a thank you message to the client.
   
    while True:
        c.send(bytes('look at me pretending to send game data!', 'ascii'))
        time.sleep(1)
        
        print(c.recv(100).decode("ascii"))
 
   # Close the connection with the client
    c.close()
    
    clientStuffGetter.join()

main()
