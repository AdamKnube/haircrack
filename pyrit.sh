#!/bin/bash
#

svn co http://pyrit.googlecode.com/svn/trunk/ pyrit
cd pyrit/pyrit
python setup.py build
sudo python setup.py install
cd ../..
