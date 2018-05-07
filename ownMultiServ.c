// import libraries(Headers in C)
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <errno.h> 
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdint.h>
#include <inttypes.h>

// MYPORT will now act as 8888 as a string in the rest of the program
#define MYPORT "8888"

// The amount of clients that can be on the server at once
#define BACKLOG 5

// Create a function to handle children
void sigchld_handler(int s)
{
	//make sure errno is saved
	int saved_errno = errno;
	
	// Wait for any child process
	while(waitpid(-1, NULL, WNOHANG) > 0);

	errno = saved_errno;
}

// seperate getting sockaddr from server and checking for IPV4/6
void *get_in_addr(struct sockaddr *sa)
{
	//Check if socket family is IPV4
	if(sa->sa_family == AF_INET) {
		//return ip as IPV4 address
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}
	
	//else return ip as IPV6 address
	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(void)
{
	//storage for client socket information
	struct sockaddr_storage their_addr;

	//size of sockaddr
	socklen_t sin_size;

	// define variables for:
	// struct addrinfo, contains socket info like 
	// ip, port and type
	struct addrinfo hints, *servinfo, *p;

	// socket file descriptor, provides connection info
	// to clients
	//new_fd is client's socket file descriptor, listen on sockfd
	int sockfd, new_fd;

	struct sigaction sa;
	//create a yes variable to return
	int yes = 1;

	// create a char that is the length of the IPV6 adress
	char s[INET6_ADDRSTRLEN];

	// variable that contains addrinfo
	int rv;

	//buffer for client message
	char client[256];
	
	//buffer for old client data
	char oldClient[256];

	//length of client data
	int clidata;

	//header info
	int data[1024];

	//client with header
	char hClient[15];

	//count for client data
	int clientChar;
	int revCC;

	//Player structs
	struct player
	{
		int team;
		int pos_x;
		int pos_y;
		int rotation;
		int health;
		int energy;
		int is_shooting;
	};

	// clear addrinfo by setting it all to zeros
	memset(&hints, 0, sizeof hints);
	memset(&client, 0, sizeof client);
	
	//load hints with info(ipv4/ipv6, tcp/udp, ip)
	hints.ai_family = AF_UNSPEC; //set to use either v4 or v6
	hints.ai_socktype = SOCK_STREAM; //set to tcp
	hints.ai_flags = AI_PASSIVE; //fill in ip automatically

	// get the rest of the info
	// (IP, Port, hints to help, struct to paste results)
	if((rv = getaddrinfo(NULL, MYPORT, &hints, &servinfo)) < 0)
	{
		//Error checking, error codes return less than 0
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	} 

	//loop for multiple clients
	for(p = servinfo; p != NULL; p = p->ai_next)
	{
		//define port as sockfd
		//socket(ipv4/6, TCP/UDP, the protocol, for most being NETINET)
		if((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) ==  -1)
		{
			perror("socket failed");
			continue;
		}

		//set socket options to reuse addresses and sockets
		//setsockopt(socket file descriptor, where to set options, option to manipulate,
		// value to set, length of value)
		if(setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) 
		{
			perror("setsockopt");
			exit(1);
		}

		//bind the socket to a port (8888) to listen for clients
		//bind(socket file descriptor, ip address, size of address struct)
		if((bind(sockfd, p->ai_addr, p->ai_addrlen)) < 0)
		{
			close(sockfd);
			perror("server: bind");
			continue;
		}

		break;
	}
	//get ready for a new client
	freeaddrinfo(servinfo);

	//check if the server is up
	if (p == NULL)
	{
		fprintf(stderr, "server: failed to bind\n");
		exit(1);
	}
	
	//tell the server to listen for clients using the listen command
	//listen(socket file descriptor, maximum amount of clients in waiting)
	if((listen(sockfd, BACKLOG)) < 0)
	{
		perror("listen");
		exit(1);
	}
	
	//remove dead processes with the function
	sa.sa_handler = sigchld_handler;
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;
	if(sigaction(SIGCHLD, &sa, NULL) == -1) 
	{
		perror("sigaction");
		exit(1);
	}

	printf("Server waiting for connections\n");

	// loop to accept clients
	while(1) 
	{
		
		//accept(server socket file descriptor, pointer to the client's address info struct,
		//size of the client's address struct, flags not used in this example
		sin_size = sizeof their_addr;
		new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
		if(new_fd == -1)
		{
			perror("accept");
			continue;
		}

		//turn client ip into text
		inet_ntop(their_addr.ss_family,
			get_in_addr((struct sockaddr *)&their_addr),
			s, sizeof s);
		//print connection made
		printf("server got a connection from %s\n", s);
		//create a child proccess for the next client
		if(!fork())
		{
			close(sockfd);
			//loop for recieving strings and sending them back
			while(1)
			{
				//previous client data is put into oldClient
				if((clidata = recv(new_fd, client, sizeof client, 0)) == -1)
					perror("recv");
				printf("%s\n", client);
				//Unmarshal data
				/*for(clientChar = 0; client[clientChar] == '\0'; clientChar++){
					if(client[clientChar] == ':'){
						for(revCC = clientChar; revCC == 0; revCC--){
							client[revCC] = '\0';
						}
					}
				}*/
				//unMarshal(hClient, data, client);
				//Send data to clients
				//send(client file descriptor, string, length of string, flags not used)
				/*if((send(new_fd, &client, strlen(client), 0)) == -1)
					perror("send back");  */
			}
			close(new_fd);
			exit(0);
		}
		close(new_fd);
	}
	return(0);
}
