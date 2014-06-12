#!/bin/bash
#

svn co http://pyrit.googlecode.com/svn/trunk/ pyrit 2>&1
cd pyrit/pyrit
python setup.py build 2>&1
sudo python setup.py install 2>&1
cd ../..
