#!/bin/bash
#

# Build script for libpcap on arch
cd libpcap-1.4.0.tar.gz
./configure --prefix=/usr
make
make install