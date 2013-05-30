#!/bin/bash
#

# Get libs for debian based distros.
# These are NOT ALL required but I consider them all to be 
# essential if you do any kind of serious building. 
#
sudo apt-get update
sudo apt-get install \
python-dev \
subversion \
build-essential \
devscripts \
automake \
autoconf \
bison \
gawk \
python-dev \
python-scapy \
libsqlite0-dev \
libsqlite3-dev \
libpcap-dev \
libssl-dev

# Now we acquire/build aircrack-ng
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
