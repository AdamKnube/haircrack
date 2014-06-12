#!/bin/bash
#

svn co http://svn.aircrack-ng.org/trunk/ aircrack
cd aircrack
make unstable=true sqlite=true
sudo make unstable=true sqlite=true install
cd ..

