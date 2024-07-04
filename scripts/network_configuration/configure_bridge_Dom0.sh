#!/bin/sh

killall -9 udhcp
ip addr del 192.168.100.60/24 dev eth0
brctl addbr xenbr0
brctl addif xenbr0 eth0
/sbin/udhcpc -i xenbr0 -b

ip route del 0.0.0.0/0 via 192.168.100.254 dev vif5.0
ip route del 0.0.0.0/0 via 192.168.100.254 dev vif7.0