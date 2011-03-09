#!/usr/bin/python

import os, sys
from ctypes import *

from kstructs import *
from memreader import *
from symbolfinder import *
from pidhash import *


###########
sf = SymbolFinder()
dm = DevMemReader(sf)

# Start by searching kallsyms for our important symbols.

ph = PidHash(sf,dm)

t = ph.find(1174)
if t != None:
	print "Found " + str(t.nr)
	t.pid_chain.remove(dm)


"""
init_task = sf.find("init_task");

dm.read(p,init_task)
print p.pid

while True:
	dm.read(p,p.next_task - 456)
	print p.pid
	#print hex(p.next_task)
	if p.pid == 0:
		break
"""
