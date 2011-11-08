#!/usr/bin/python

"""
Find a dentry based on a file name.

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

import version
exec("from dorf."+version.my_version+".kstructs import *")
exec("from dorf."+version.my_version+".memreader import *")
exec("from dorf."+version.my_version+".symbolfinder import *")

from dorf.hashtable.dentryhash import *


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


"""
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
"""
