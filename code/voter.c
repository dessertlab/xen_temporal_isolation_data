#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <pthread.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include "rt-lib.h"

#define PERIOD 20000	// Period in microseconds
#define N 2000  		// Number of sent messages in a run

static int port_a;
static int port_b;

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


int CreaSocket(int Porta)
{
  int sockfd,errore;
  struct sockaddr_in serv_addr;
  const int enable = 1;

  //Creazione socket (scelgo il protocollo da usare)
  sockfd=socket(AF_INET,SOCK_STREAM,0); //IPV4 protocol TCP
  if(sockfd == -1){
	  printf("Can't create socket\n");
	  return -1;
  }

  //Reuse PORT and ADDR
  if(setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int))<0){
	  printf("setsockopt(SO_REUSEADDR) failed");
  }
  if(setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, &enable, sizeof(int))<0){
  	  printf("setsockopt(SO_REUSEPORT) failed");
  }

  //Tipo di indirizzo
  serv_addr.sin_family=AF_INET;
  serv_addr.sin_addr.s_addr=INADDR_ANY;
  serv_addr.sin_port=htons(Porta);

  //Il socket deve essere bloccante (quindi non va inserito il flag O_NOBLOCK)
  errore=fcntl(sockfd,F_SETFL,0);

  //Bind del socket
  errore=bind(sockfd,(struct sockaddr*) &serv_addr,sizeof(serv_addr));

  //Listen, il server si mette in ascolto sul socket creato
  errore=listen(sockfd,7);
  if(errore == -1){
	  printf("Error: CreaSocket fail.\n");
	  return -1;
  }

  return sockfd;
}

void ChiudiSocket(int sock)
{
  close(sock);
  return;
}

int checkMsg(int newsockfd, char buffer[512], int* queue)
{
	int exitCond=0;
	int dim=0;


	if ((dim=read(newsockfd,buffer,5))<0)
	{
		printf("Impossibile leggere il messaggio.\n");
		ChiudiSocket(newsockfd);
	}
	else
	{
		*queue=1;
		//printf("buffer:%s\n",buffer);
		if (strncmp(buffer,"exit",5)==0)
		exitCond=1;
	}
	return exitCond;
}

void* voter_loop(void* par){
	FILE *fptr;
	FILE *file_sock1;
	FILE *file_sock2;
	FILE *file_newsock1;
	FILE *file_newsock2;

	// Buffer to receive and send messages
	char buffer1[512];
	char buffer2[512];
	char resp[256];
	// Socket descriptors
	int sockfd1, sockfd2;
	int newsockfd1, newsockfd2;
	socklen_t clilen1,clilen2;
	struct sockaddr_in client_addr1, client_addr2;
	// Time
	long long finish=0;
	long long start=0;
	long long diff[N];
	struct timespec now;
	// Utility var
	int exitCond=0;
	int exitFirst=0;
	int exitSecond=0;
	int queue1=0;
	int queue2=0;
	int i= 0;
	int check = 0;
	int counter = 0;
	int fail_counter = 0;
	int deadline_counter = 0;


	//Create Socket on chosen ports
	sockfd1=CreaSocket(port_a);
	sockfd2=CreaSocket(port_b);
	if(sockfd1==-1 || sockfd2==-1){
		printf("Error: Socket cannot be create\n");
		pthread_exit(NULL);
	}

	//Wait for replica_A and replica_B to connect
	printf("Server: Attendo connessioni...\n");
	clilen1 = sizeof(client_addr1);
	clilen2 = sizeof(client_addr2);
	newsockfd1 =accept(sockfd1,(struct sockaddr*)&client_addr1,&clilen1);
	newsockfd2 =accept(sockfd2,(struct sockaddr*)&client_addr2,&clilen2);

	file_sock1 = fdopen(sockfd1,"w");
	file_sock2 = fdopen(sockfd2,"w");
	file_newsock1 = fdopen(newsockfd1,"w");
	file_newsock2 = fdopen(newsockfd2,"w");

	// Send a message to the clients to sync
	sprintf(resp, "Start!");
    write(newsockfd1, resp, strlen(resp));
    write(newsockfd2, resp, strlen(resp));
    printf("Start!\n");

	periodic_thread *th = (periodic_thread *) par;
    start_periodic_timer(th,PERIOD);

	while (i<N)
	{
		//printf("i:%d",i);
		wait_next_activation(th);
		start=timeInNano();

		// Active wait of messages from clients
		if(queue1==0)
		  exitFirst = checkMsg(newsockfd1, buffer1, &queue1);

		if(queue2==0)
		  exitSecond = checkMsg(newsockfd2, buffer2, &queue2);

		//Verify exit condition
		exitCond=exitFirst+exitSecond;

		// Check the received messages
		if (queue1==1 && queue2==1 && !exitCond)
		{
			if (strncmp(buffer1,buffer2,5)==0){
				counter++;
			}
			else{
				fail_counter++;
			}
			bzero(buffer1,512);
			bzero(buffer2,512);
		}
		queue1=queue2=0;

		//Take time
		finish=timeInNano();
		diff[i] = (finish-start);
		i++;

		//Check that the iteration ends before the end of its period
		clock_gettime(CLOCK_REALTIME, &(now));
		if(compare_time(&now,&(th->r))){ //if((finish-start) > PERIOD/1000){
				//printf("DEADLINE MISS!\n");
			deadline_counter++;
		}
	}
	printf("Saving on file...\n");
	//Save on file
	fptr = fopen("finish.txt", "a");
	for(i = 0; i < N; i++){
		check = fprintf(fptr, "%llu\n", diff[i]);
		if (check<0){
			printf("Errore in scrittura\n");
			exit(1);
		}
	}

	//Print results
	printf("counter = %d \t fail = %d \t tot = %d\t",counter, fail_counter, (counter+fail_counter));
	printf("Deadline miss counter: %d\n",deadline_counter);

	//Clear files and close descriptors
	fflush(file_sock1);
	fflush(file_sock2);
	fflush(file_newsock1);
	fflush(file_newsock2);
	fclose(fptr);
	ChiudiSocket(sockfd1);
	ChiudiSocket(sockfd2);
	ChiudiSocket(newsockfd1);
	ChiudiSocket(newsockfd2);
	printf("Server: Terminato.\n");

	pthread_exit(NULL);
}

int main(int argc,char* argv[])
{
  // Take two input value from command line to define the listen ports
  if(argc != 3){
	  char argc_error[200] = "ERROR: Entered more/less than two input string. You must input two input strings into the command line: port_a port_b";
  	  fprintf(stderr, "%s\n", argc_error);
  	  return 0;
  }
  port_a = atoi(argv[1]);
  port_b = atoi(argv[2]);
  printf("entered[voter] -> port_a:%d \t port_b:%d\n",port_a,port_b);

  // Init thread attr.
  pthread_t voter_thread;
  pthread_attr_t myattr;
  struct sched_param myparam;

  pthread_attr_init(&myattr);
  pthread_attr_setschedpolicy(&myattr, SCHED_FIFO);
  pthread_attr_setinheritsched(&myattr, PTHREAD_EXPLICIT_SCHED);

  // VOTER THREAD
  periodic_thread voter_th;
  voter_th.period = PERIOD;
  voter_th.priority = 50;

  myparam.sched_priority = voter_th.priority;
  pthread_attr_setschedparam(&myattr, &myparam);
  pthread_create(&voter_thread,&myattr,voter_loop,(void*)&voter_th);

  pthread_attr_destroy(&myattr);

  //Wait voter_thread to finish
  pthread_join(voter_thread,NULL);

  return 0;
}
