#!/bin/bash
#

svn co http://reaver-wps.googlecode.com/svn/trunk/ reaver 2>&1
cd reaver/src
./configure 2>&1
make 2>&1
sudo make install 2>&1
cd ../..

