#!/bin/bash
#

svn co http://svn.aircrack-ng.org/trunk/ aircrack 2>&1
cd aircrack
make unstable=true sqlite=true 2>&1
sudo make unstable=true sqlite=true install 2>&1
cd ..

