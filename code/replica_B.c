#include <sys/types.h>
#include <sys/socket.h>
//"in" per "sockaddr_in"
#include <netinet/in.h>
//"netdb" per "gethostbyname"
#include <netdb.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <inttypes.h>
#include <math.h>
#include <fcntl.h>
#include <string.h>
#include <pthread.h>
#include "rt-lib.h"

#define PERIOD 20000 //Period in microseconds
#define N 2000		// Number of messages to send

//Static Variables
static char *IP;
static int port;


long long timeInMicro(void) {
  struct timespec spec;
  clock_gettime(CLOCK_REALTIME, &spec);
  return (((long long)spec.tv_sec)*1000000)+(spec.tv_nsec/1000);

}

long long timeInNano(void) {
  struct timespec spec;
  clock_gettime(CLOCK_REALTIME, &spec);
  return (((long long)spec.tv_sec)*1000000000)+(spec.tv_nsec);

}

void ChiudiSocket(int sock)
{
  close(sock);
  return;
}

int CreaSocket(char* Destinazione, int Porta)
{
  struct sockaddr_in server_addr;
  struct hostent *server;
  int sockfd;
  int errore;

  //Create socket.
  sockfd=socket(AF_INET,SOCK_STREAM,0);
  if(sockfd == -1){
	  printf("Can't create socket\n");
	  return -1;
  }

  server=gethostbyname(Destinazione);
  if (server == NULL) {
      printf("ERROR, no such host\n");
      return -1;
  }

  bzero((char *) &server_addr, sizeof(server_addr));
  server_addr.sin_family=AF_INET;
  server_addr.sin_port=htons(Porta);
  bcopy((char *)server->h_addr,(char *)&server_addr.sin_addr.s_addr,server->h_length);


  //Socket connection
  errore=connect(sockfd, (struct sockaddr*) &server_addr, sizeof(server_addr));
  if(errore == -1){
	  printf("Error: CreaSocket fail.\n");
	  return -1;
  }

  return sockfd;
}

void SpedisciMessaggio(int sockfd, char* Messaggio)
{
  //printf("Client: %s\n",Messaggio);
  if (write(sockfd,Messaggio,strlen(Messaggio))<0)
  {
    printf("Impossibile mandare il messaggio.\n");
    ChiudiSocket(sockfd);
    exit(1);
  }
  return;
}


void* replica_loop(void* par){
	FILE *fptr;
	FILE *file_sock;
	// socket file descriptor
	int sockfd;
	// Buffer for messages
	char buffer[512];
	char messaggio1[5]= "1000";
	char messaggio2[5]= "1005";
	char exit_message[5]= "exit";
	//Time
	long long start;
	long long finish;
	long long diff[N];
	//Utility
	int i=0;

	//Communication channel creation using sockets
	sockfd=CreaSocket(IP,port);
	if(sockfd == -1){
		printf("Error: Socket cannot be create\n");
		pthread_exit(NULL);
	}
	file_sock = fdopen(sockfd,"w");

	//Wait the Voter signal to sync
	int dim = read(sockfd, buffer, 512);

	periodic_thread *th = (periodic_thread *) par;
    start_periodic_timer(th,0);

	while(i<N)
	{
		wait_next_activation(th);
		start=timeInNano();

		srand(time(NULL));
		//Do random calculation and send results
		if(rand()%2==0)
		  SpedisciMessaggio(sockfd,messaggio1);
		else
		  SpedisciMessaggio(sockfd,messaggio2);

		finish = timeInNano();
		diff[i] = (finish - start);
		i++;
	}
	wait_next_activation(th);
	SpedisciMessaggio(sockfd,exit_message);

	//Write on file
	fptr = fopen("start2.txt", "a");
	if(fptr==NULL)
	{
	  printf("errore nell'apertura del file. Exit");
	  exit(1);
	}
	for(i = 0; i < N; i++){
		int check = fprintf(fptr, "%llu \n", diff[i]);
		if(check<0)
		{
		  printf("errore nella scrittura su file. Exit");
		  exit(1);
		}
	}
	fflush(file_sock);
	ChiudiSocket(sockfd);
	pthread_exit(NULL);
}

int main(int argc,char* argv[])
{

  if(argc != 3){
	  char argc_error[200] = "ERROR: Entered more/less than two input string. You must input two input strings into the command line: IP port";
	  fprintf(stderr, "%s\n", argc_error);
	  return 0;
  }
  IP = argv[1];
  port = atoi(argv[2]);
  printf("entered [replica_B]-> IP:%s \t port:%d\n",IP,port);

  // Init thread attr.
  pthread_t replica_thread;
  pthread_attr_t myattr;
  struct sched_param myparam;

  pthread_attr_init(&myattr);
  pthread_attr_setschedpolicy(&myattr, SCHED_FIFO);
  pthread_attr_setinheritsched(&myattr, PTHREAD_EXPLICIT_SCHED);

  // REPLICA THREAD
  periodic_thread replica_th;
  replica_th.period = PERIOD;
  replica_th.priority = 50;

  myparam.sched_priority = replica_th.priority;
  pthread_attr_setschedparam(&myattr, &myparam);
  pthread_create(&replica_thread,&myattr,replica_loop,(void*)&replica_th);

  pthread_attr_destroy(&myattr);

  //Wait replica_thread to finish
  pthread_join(replica_thread,NULL);

  return 0;
}

