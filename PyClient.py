# For my Computer, makes it run without specifying python
#!/usr/bin/python3

#socket lib import
import socket

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
	msg = s.recv(100)
	#decodes the message in ascii
	print(msg.decode('ascii'))
	#close the connection to the server
	s.close()

main()
