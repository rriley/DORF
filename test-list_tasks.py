#!/usr/bin/python

"""
List all items in the process list.

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

import version
exec("from dorf."+version.my_version+".kstructs import *")
exec("from dorf."+version.my_version+".memreader import *")
exec("from dorf."+version.my_version+".symbolfinder import *")

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
