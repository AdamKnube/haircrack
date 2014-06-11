#!/usr/bin/perl
#


use strict;

my @packages;
my $dist = `uname -a`;

if (($dist =~ /ubuntu/) || ($dist =~ /debian/)) { 
  print "Building for Ubuntu Linux.\n";
  # Get libs for debian based distros.
  print "Acquiring updated package lists...\n";
  system('sudo apt-get update');
  print "Acquiring packages...\n";
  $packages[0] = 'sudo apt-get install';
  $packages[1] = 'python-dev';
  $packages[2] = 'subversion';
  $packages[3] = 'build-essential';
  $packages[4] = 'devscripts';
  $packages[5] = 'automake';
  $packages[6] = 'autoconf';
  $packages[7] = 'bison';
  $packages[8] = 'gawk';
  $packages[9] = 'python2-dev';
  $packages[10] = 'python-scapy';
  $packages[11] = 'libsqlite0-dev';
  $packages[12] = 'libsqlite3-dev';
  $packages[13] = 'cmake';
  $packages[14] = 'libpcap-dev';
  $packages[15] = 'libssl-dev'; 
  $packages[16] = 'libnl-dev';
  $packages[17] = 'python-distutils-extra';
  $packages[18] = 'python2-distutils-extra';
}
elsif ($dist =~ /ARCH/) {
  print "Building for Arch Linux.\n";
  # Get libs for arch based distros.
  print "Acquiring updated package lists...\n";
  system('sudo pacman -Sy');
  print "Acquiring packages...\n";
  $packages[0] = 'sudo pacman -S';
  $packages[1] = 'base-devel';
  $packages[2] = 'subversion';
  $packages[3] = 'cmake';
  $packages[4] = 'autoconf';
  $packages[5] = 'automake';
  $packages[6] = 'bison';
  $packages[7] = 'gawk';
  $packages[8] = 'scapy';
  $packages[9] = 'python2-distutils-extra';
  $packages[10] = 'sqlite';
  $packages[11] = 'libpcap';
  $packages[12] = 'openssl';
  $packages[13] = 'libnl';
  $packages[14] = 'python-distutils-extra';
}
else { die "Error: Don't know how to build for \"$dist\"\n"; }

my $getpacks = join(' ', @packages);
system($getpacks);
exit(0);
