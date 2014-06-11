#!/bin/bash
#

# Acquire/build aircrack-ng
svn co http://svn.aircrack-ng.org/trunk/ aircrack
cd aircrack
make unstable=true sqlite=true
sudo make unstable=true sqlite=true install
cd ..

# Same thing for reaver
svn co http://reaver-wps.googlecode.com/svn/trunk/ reaver
cd reaver/src
./configure
make
sudo make install
cd ../..

# Finally is pyrit
svn co http://pyrit.googlecode.com/svn/trunk/ pyrit
cd pyrit/pyrit
python setup.py build
sudo python setup.py install
cd ../..
