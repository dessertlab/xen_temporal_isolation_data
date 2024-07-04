#!/bin/bash
nome=$1
n_exp=$2
IP_DOM0=192.168.100.68
IP_A=192.168.100.66
IP_B=192.168.100.67
PORT_A=1745
PORT_B=1746
period=(5000 9000 10000 10000)
budget=(1000 3000 5000 10000)
ratelimit=(100 500 1000 5000)

# Create Directory for the results
rm -rf results/${nome} && mkdir -p results/${nome}
echo "Creating directory: ${nome}"

# Delete ssh known host if needed
sed -i '$ d' /home/root/.ssh/known_hosts
sed -i '$ d' /home/root/.ssh/known_hosts

# For each scheduler parameter
for((j=0;j<1;j++)) do

        # Create Directory
        rm -rf results/${nome}/$((j+1)) && mkdir -p results/${nome}/$((j+1))
        echo "Creating directory: ${nome}/$((j+1)) "
        echo "Launching ${n_exp} experiments..."

        # Send the script and the code to DomUs
        scp -i /etc/dropbear/id_rsa exe_code/replica_A.elf root@$IP_A:/root #/${nome}
        scp -i /etc/dropbear/id_rsa script/script_A.sh     root@$IP_A:/root #/${nome}
        scp -i /etc/dropbear/id_rsa exe_code/replica_B.elf root@$IP_B:/root #/${nome}
        scp -i /etc/dropbear/id_rsa script/script_B.sh     root@$IP_B:/root #/${nome}

        # For rach replica 
        for((i=0;i<${n_exp};i++)) do
                echo "replica $((i+1)) starts: "
		rm -rf finish.txt

                # Create Directory
                mkdir results/${nome}/$((j+1))/rep$((i+1))

                # start Voter
                ./exe_code/voter $PORT_A $PORT_B & 
		pid_voter=$!

                # start Scripts on VMs
                ssh -i /etc/dropbear/id_rsa root@$IP_A sh /root/script_A.sh $IP_DOM0 $PORT_A &
                ssh -i /etc/dropbear/id_rsa root@$IP_B sh /root/script_B.sh $IP_DOM0 $PORT_B &

                # wait results
                echo "waiting for process $pid_voter..."
                wait $pid_voter
		
		# sleep
                sleep 1

                # take DomO results in the same folder
                scp -i /etc/dropbear/id_rsa root@$IP_A:/root/start.txt results/${nome}/$((j+1))/rep$((i+1))
                scp -i /etc/dropbear/id_rsa root@$IP_B:/root/start2.txt results/${nome}/$((j+1))/rep$((i+1))
                mv finish.txt results/${nome}/$((j+1))/rep$((i+1))
        done
done

# Clear
rm -rf finish.txt