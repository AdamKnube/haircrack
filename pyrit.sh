#!/bin/bash
#

svn co http://pyrit.googlecode.com/svn/trunk/ pyrit 2>&1
cd pyrit/pyrit
python2 setup.py build 2>&1
sudo python2 setup.py install 2>&1
cd ../..
