#!/usr/bin/python

"""
Test to see if we are finding bh_lrus properly.

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


if len(sys.argv) != 1:
	print "Usage: ",
	print sys.argv[0]
	sys.exit(-1)

# Declare our necessary pieces for this attack
sf = SymbolFinder()
dm = DevMemReader(sf)
bh_lrus = sf.find("bh_lrus")

print "bh_lrus: " + hex(bh_lrus)

bh = buffer_head()

# Read the item's parent dir, this causes the block related to it
# to end up at the head of the bh_lrus list.  Very convenient...
# This might not work under heavy workloads, multi-core, etc.
# (But it can be changed to handle multicore...)
print os.listdir(".")

# Read in the first buffer_head from the LRU
# The offset is kernel specific and stored with the buffer_head
bh_addr = dm.read_int(bh_lrus + 0x1cbb7000)

print "bh_addr: " + hex(bh_addr)

dm.read(bh, bh_addr)

# Go through the directory block and find the entry, then
# remove it.
# This will probably fail for large directories with more than
# one block used to store their children...

de = dir_entry()
de_p = dir_entry()
i = bh.b_data
prev = 0
print "Count: ",
print hex(bh.b_count)

while True:
	dm.read(de, i)
	if de.inode > 0:
		print bh.b_data+i,
		print de.inode,
		print de.rec_len,
		print de.name_len,
		print de.file_type,

		fname= dm.read_bytes(i+8,de.name_len)
		print fname

		prev = i
		i += de.rec_len
		if i >= bh.b_data+bh.b_size:
			break
	else:
		print "Done!"
		break;
