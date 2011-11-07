#!/usr/bin/python

"""
List all items in the process list.

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

from dorf.ubuntu910.kstructs import *
from dorf.ubuntu910.memreader import *
from dorf.ubuntu910.symbolfinder import *

if len(sys.argv) != 1:
	print "Usage: ",
	print sys.argv[0]
	sys.exit(-1)

sf = SymbolFinder()
dm = DevMemReader(sf)

p = task_struct()

init_task = sf.find("init_task")
dm.read(p,init_task)
dm.read(p,p.next())

while p.pid != 0:
	dm.read(p,p.next())
	print p.pid
