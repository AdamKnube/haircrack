#!/usr/bin/perl
#
# Still got a long way to go...
# Need to label dependancies for what tool they belong to
# and then only install those depends. For now it only 
# pays attention to reaver. If reaver is installed then
# we assume libpcap needs removing and recompiling.
#

# Includes
use strict;
use Getopt::Long;

# Globals
my $reav = 0;
my $airc = 0;
my $pyrt = 0;
my $iall = 1;
my $debug = 0;
my $pfil = '';
my $pman = '';
my $pupc = '';
my $pinc = '';
my $prem = '';
my $ddat = '';

# Initialize
GetOptions(
  'debug+' => \$debug,
  'aircrack+' => \$airc,
  'reaver+' => \$reav,
  'pyrit+' => \$pyrt
);
if ($reav || $airc || $pyrt) { $iall = 0; }
my $dist = `uname -a`;
if ($dist =~ /ubuntu/) {
  dprint('Installing for Ubuntu Linux.');
  $pfil = 'ubuntu.pre';
  $pman = 'apt-get';
  $pupc = 'update';
  $pinc = '--noconfirm install';
  $prem = 'purge libpcap libpcap-dev';
}
elsif ($dist =~ /ARCH/) {
  dprint('Installing for Arch Linux.');
  $pfil = 'arch.pre';
  $pman = 'pacman';
  $pupc = '-Sy';
  $pinc = '-S --needed';
  $prem = '-Rdd libpcap';
}
else { die "Error: Don't know how to build for \"$dist\"\n"; }

# Update the system package lists
dprint('Acquiring updated package lists..');
$ddat = `sudo $pman $pupc 2>&1`;
dprint($ddat, 1);

# Get the required packages
my @paklist;
dprint('Reading package list...');
open(PAKLIST, "<", $pfil) || die "Error: Can't find $pfil!\n";
my @paks = <PAKLIST>;
close(PAKLIST);
foreach my $pak (@paks) {
  $pak =~ s/^\s+//;
  $pak =~ s/\s+$//; 
  $pak =~ s/\n//;
  if (($pak !~ /^#/) && ($pak ne '')) { push(@paklist, $pak); }
}
dprint('Acquiring packages...');
my $joiner = "sudo $pman $pinc " . join(' ',@paklist) . ' 2>&1';
if ($dist =~ /ARCH/) { $joiner = 'echo n | ' . $joiner; }
$ddat = `$joiner`;
dprint($ddat, 1);

# Remove and downgrade libpcap if required
if ($reav || $iall) { 
  dprint('Removing libpcap...');
  $ddat = `sudo $pman $prem 2>&1`;
  dprint($ddat, 1);
  dprint('Installing libpcap1.4.0...'); 
  $ddat = `./pcap.sh`;
  dprint($ddat, 1);
}

# Install the requested/required tools
dprint('Installing required/requested tools...');
if ($airc || $iall) { 
  $ddat = `./aircrack.sh`; 
  dprint($ddat, 1);
}
if ($reav || $iall) { 
  $ddat = `./reaver.sh`;
  dprint($ddat, 1);
}
if ($pyrt || $iall) {
  $ddat = `./pyrit.sh`;
  dprint($ddat, 1);
}

# Death by natural causes
exit(0);

# Functions/Subs
sub dprint() {
  my $data = shift;
  my $levl = shift;
  if ($levl >= $debug) { print "$data\n"; }
  if ($debug > 1) {
	my $trampstamp = `date +[%m/%d/%y-%H:%M:%S]`;
	open(LOGG, ">>", "$0.log") || die "Can't open() the logfile\n";
	print LOGG $trampstamp . " $data\n";
	close(LOGG);
  }
}
