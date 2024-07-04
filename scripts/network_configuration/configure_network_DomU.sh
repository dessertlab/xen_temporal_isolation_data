#!/bin/sh

# Start sshd (device null problem)
rm /dev/null
mknod /dev/null c 1 3
echo PermitRootLogin yes >> /etc/ssh/sshd_config
mkdir /root/.ssh
touch /root/.ssh/authorized_keys
echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCfQX30S2/vWAV4vhEo5nzNEoJ1uObYcdLS/WUnRg4U9denHyHhl6Wuwl2djbRaQgt6eFMLLB1FVIhMF7nacXnoSdrrWj2XKn8grZ+h/W6eSJ3Se3T092qenO04hzsjJrfUO+WbUFg+LB2oF0naJw7uVXxJx/lLdvFKZA6BPVpOS5RPoN1VvES//1LYtNg7bLlE3ftZgPdikGILtH+qLwtl72qePEFevCFUID0FCIvBkSz9y6hRFudzJrCa016DkWB1lNVQRlvv6sQ7L8/8OYqYnhrCerVHKoGsWM92R/ixtmQaimwhYRlCcghfgglL4TiNFrFQWfEgMxxg2xQZvI/3 root@xilinx-zcu104-20221 > /root/.ssh/authorized_keys

sh /etc/init.d/S50sshd restart

# crea IP e tabella di routing
ip addr add 192.168.100.66/24 dev eth0
ip link set eth0 up
ip route add 0.0.0.0/0 via 192.168.100.254 dev eth0
route -n