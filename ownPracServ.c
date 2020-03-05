// import libraries(Headers in C)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <errno.h>
#include <netinet/in.h>
#include <netdb.h>

// MYPORT will now act as 8888 as a string in the rest of the program
#define MYPORT "8888"

int main(void)
{
	//storage for client socket information
	struct sockaddr_storage their_addr;
	socklen_t addr_size;
	// define variables for:
	// struct addrinfo, contains socket info like 
	// ip, port and type
	struct addrinfo hints, *res;
	// socket file descriptor, provides connection info
	// to clients
	//new_fd is client's socket file descriptor
	int sockfd, new_fd;
	//Message to send
	char *message = "This is how you make a server in C!\r\n";

	// clear addrinfo by setting it all to zeros
	memset(&hints, 0, sizeof hints);
	//load hints with info(ipv4/ipv6, tcp/udp, ip)
	hints.ai_family = AF_UNSPEC; //set to use either v4 or v6
	hints.ai_socktype = SOCK_STREAM; //set to tcp
	hints.ai_flags = AI_PASSIVE; //fill in ip automatically

	// get the rest of the info
	// (IP, Port, hints to help, struct to paste results)
	if((getaddrinfo(NULL, MYPORT, &hints, &res)) < 0)
	{
		//Error checking, error codes return less than 0
		perror("getaddr failed");
		exit(EXIT_FAILURE);
	} 

	//define port as sockfd
	//socket(ipv4/6, TCP/UDP, the protocol, for most being NETINET)
	if((sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol)) < 0)
	{
		perror("socket failed");
		exit(EXIT_FAILURE);
	}

	//bind the socket to a port (8888) to listen for clients
	//bind(socket file descriptor, ip address, size of address struct)
	if((bind(sockfd, res->ai_addr, res->ai_addrlen)) < 0)
	{
		perror("bind failed");
		exit(EXIT_FAILURE);
	}

	//tell the server to listen for clients using the listen command
	//listen(socket file descriptor, maximum amount of clients in waiting)
	if((listen(sockfd, 3)) < 0)
	{
		perror("listen failed");
		exit(EXIT_FAILURE);
	}

	//start accepting clients
	//define size of the client's address struct
	addr_size = sizeof their_addr;
	//define new_fd as the client's connection
	//accept(server socket file descriptor, pointer to the client's address info struct,
	//size of the client's address struct, flags not used in this example
	if((new_fd = (accept(sockfd, (struct sockaddr *)&their_addr, &addr_size))) < 0)
	{
		perror("accept");
		exit(EXIT_FAILURE);
	}

	//Send data to clients
	//send(client file descriptor, string, length of string, flags not used)
	if(send(new_fd, message, strlen(message), 0) != strlen(message))
	{
		perror("send");
	}
}
