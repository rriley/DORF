import os, sys
from ctypes import *

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
