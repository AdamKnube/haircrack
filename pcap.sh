#!/bin/bash
# 

#libpcap install script
wget http://www.tcpdump.org/release/libpcap-1.4.0.tar.gz
tar -xvf libpcap-1.4.0.tar.gz
cd libpcap-1.4.0
./configure --prefix=/usr
make
sudo make install
