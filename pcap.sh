#!/bin/bash
# 

#libpcap install script
wget http://www.tcpdump.org/release/libpcap-1.4.0.tar.gz 2>&1
tar -xvf libpcap-1.4.0.tar.gz 2>&1
cd libpcap-1.4.0
./configure --prefix=/usr 2>&1
make 2>&1
sudo make install 2>&1
cd ..
