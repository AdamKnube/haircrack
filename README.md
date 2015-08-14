haircrack v0.3a
================

Description:
-------------
  An interface for aircrack/reaver/pyrit written in python. The interface itself
may never get finished. For right now the main goal is on a seamless install
of all the required tools and libraries that hair.py relies on. As a secondary
objective it needs to work on both ubuntu and arch linux.


History:
---------
  0.0 - First release barely works.
  0.1 - Fixed aircrack SVN download link.
  0.2 - Changed the installer from bash to perl and added some portability.
  0.3a - libpcap seems broken these days so added scripts to downgrade it.
  0.3b - libpcap is fixed, and also debian changed some package names

Todo:
------
  - Re-write the setup in python to properly catch the output.
  - Downgrade scripts for ubuntu.
  - Finish the hair.py.
  - Maybe add some more distros to the installer (yum/yast/wget-config-make/etc).


Usage:
------------
  - Install pre-requisites are perl (new) and python3.
  - Run 'setup.sh' the installer will take care of the rest or die() trying.
  - After all the tools are installed run hair.py.
