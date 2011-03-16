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
	print " <name to find>"
	sys.exit(-1)

sf = SymbolFinder()
dm = DevMemReader(sf)


bh = buffer_head()
bh_lrus = sf.find("per_cpu__bh_lrus")

print sizeof(bh)
print hex(bh_lrus)
print "---"
# Read the directory, then get the list...
print os.listdir("/usr/local/MonkeyGreen")

#for i in range(0, 8):
bh_addr = dm.read_int(bh_lrus + 0x04bf2000)
dm.read(bh, bh_addr)
print bh,
print "---"

buf = dm.read_bytes(bh.b_data, bh.b_size)
of = open("page-0", "w")
of.write(buf)
of.close()

de = dir_entry()
i = 0
while True:
	dm.read(de, bh.b_data+i)
	if de.inode > 0:
		print bh.b_data+i,
		print de.inode,
		print de.rec_len,
		print de.name_len,
		print de.file_type,
		fname= dm.read_bytes(bh.b_data+i+8,de.name_len)
		print fname
		#print
		if fname == "john":
			print "found it!"
			de.rec_len=32
			dm.write(de, bh.b_data+i)
		i += de.rec_len
		if i >= bh.b_size:
			break
	else:
		print "Done!"
		break;
