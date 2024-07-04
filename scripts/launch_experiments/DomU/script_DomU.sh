#!/bin/sh

IP=$1
port=$2

rm -rf start.txt
./replica_A.elf $IP $port
