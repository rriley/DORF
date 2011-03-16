#!/usr/bin/python

"""
FUULD testing program for dealing with dentries
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
from dentryhash import *


if len(sys.argv) != 2:
	print "Usage: ",
	print sys.argv[0],
	print " <name to find>"
	sys.exit(-1)

sf = SymbolFinder()
dm = DevMemReader(sf)


dh = DentryHash(sf,dm)

#dh.print_all()
print "---"
t = dh.find(sys.argv[1])
if t != None:
	print "Found " + str(t)
	print "Parent subdirs.next: " + hex(t.d_subdirs.next)
	print "Parent subdirs.prev: " + hex(t.d_subdirs.prev)


	if t.d_subdirs.next != t.d_subdirs.prev:
		item = dentry()
		item.set_dm(dm)
		tptr = t.d_subdirs.next
		dm.read(item, tptr-item.child_offset)
		done = item.d_child.prev
		while True:
			print str(item),
			print len(str(item)),

                        if str(item) == "arghy":
                                print "Yes!"
				item.d_child.remove(dm)
                        else:
                                print "Nope!"


			tptr = item.d_child.next	
			if tptr == done:
				break;

			dm.read(item, tptr-item.child_offset)
