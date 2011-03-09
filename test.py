#!/usr/bin/python

import os, sys
from ctypes import *

class DevMemReader:
	def __init__(self):
		self.fd = open("/dev/mem","rb")

	def read(self, dest, addr):
		self.fd.seek(addr-0xc0000000)
		self.fd.readinto(dest)

class TaskStruct(Structure):
	_fields_ = [ 	('junk1',c_char * 456), 
			('next_task',c_void_p), 
			('prev_tast',c_void_p),
			('junk2',c_char * 56),
			('pid', c_int)
		   ]

dm = DevMemReader()
p = TaskStruct()

# Start by searching kallsyms for our important symbols.
ks = open("/proc/kallsyms", "rb")
for line in ks:
	if line.endswith(" init_task\n"):
		init_task = int(line.split(' ')[0], 16)
ks.close()

dm.read(p,init_task)
print p.pid
print hex(p.next_task)

while True:
	dm.read(p,p.next_task - 456)
	print p.pid
	print hex(p.next_task)
	if p.pid == 0:
		break
