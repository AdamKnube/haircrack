#!/bin/bash
#

svn co http://reaver-wps.googlecode.com/svn/trunk/ reaver
cd reaver/src
./configure
make
sudo make install
cd ../..

