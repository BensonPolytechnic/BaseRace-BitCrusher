# For my Computer, makes it run without specifying python
#!/usr/bin/python3

#socket lib import
import socket, time

def main():
	#creates a socket that uses regular IP and TCP
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#lets the user specify the IP of the server, 127.0.0.1 for testing
	host = str(input("What is the IP of the server?"))
	#connects to the same port as the C server
	port = 8888
	#Connects on the last two variables
	s.connect((host, port))
	#recieves message from the server, up to 100 bytes
	while True:
            time.sleep(1)
            s.send(bytes("1", "ascii"))
            msg = s.recv(100)
            print(msg.decode('ascii'))
	#close the connection to the server

main()
