import os, sys
from ctypes import *

class list_head(Structure):
	_fields_ = [	('next', c_uint),
			('prev', c_uint)
		   ]

        def remove(self, dm):
                prev = list_head()
                next = list_head()

                if self.prev != 0:
                        dm.read(prev, self.prev)
                        prev.next = self.next
                        dm.write(prev, self.prev)

                if self.next != 0:
                        dm.read(next, self.next)
                        next.prev = self.prev
                        dm.write(next, self.next)

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
	list_offset = 36

	_fields_ = [	('junk1', c_char * 28),
			('nr', c_int),
			('ns', c_void_p),
			('pid_chain', hlist_node)
		   ]

	def __str__(self):
		return "PID: " + str(self.nr)

	def next(self):
		return self.pid_chain.next

	def pprev(self):
		return self.pid_chain.pprev

	def compare(self, thing):
		return thing-self.nr

class task_struct(Structure):
	list_offset = 432

	_fields_ = [ 	('junk1',c_char * 432), 
			('tasks',list_head), 
			('junk2',c_char * 68),
			('pid', c_int)
		   ]
	def prev(self):
		return self.tasks.prev - self.list_offset

	def next(self):
		return self.tasks.next - self.list_offset

class qstr(Structure):
	_fields_ = [	('hash', c_int),
			('len', c_int),
			('name', c_void_p)
		   ]

	def get_string(self, dm):
		return dm.read_bytes(self.name, self.len)		

class dentry(Structure):
	list_offset = 20
	subdirs_offset = 60
	child_offset = 52

	_fields_ = [	('d_count', c_uint),
			('d_flags', c_uint),
			('junk1', c_char*8),
			('d_inode', c_void_p),
			('d_hash', hlist_node),
			('d_parent', c_void_p),
			('d_name', qstr),
			('junk2', c_char*8),
			('d_child', list_head),
			('d_subdirs', list_head),
			('junk3', c_char*28),
			('d_iname', c_char*32)
		   ]

	dm = None

	def set_dm(self, dm):
		self.dm = dm

	def __str__(self):
		return self.d_name.get_string(self.dm)

	def next(self):
		return self.d_hash.next

	def pprev(self):
		return self.d_hash.pprev

	def compare(self, thing):
		me = self.__str__()
		return (thing > me) - (thing < me)

class buffer_head(Structure):
	_fields_ = [	('b_state', c_uint),
			('junk1', c_uint),
			('b_page', c_uint),
			('b_blocknr', c_uint64),
			('b_size', c_uint),
			('b_data', c_uint),
			('junk2', c_uint*6),
			('b_count', c_uint)
		   ]

	# Return the address to the first buffer head.
	# This is kernel dependent, so it moves here.
	# The offset below is found by the kernel module
	def get_addr_first_bh(self, sf):
		bh_lrus = sf.find("bh_lrus")
		return bh_lrus+0x1e88a000

	def __str__(self):
		s = ""

		for i in range(0,2):
			s += ("junk1["+str(i)+"]: " + hex(self.junk1[i]) + "\n")

		s += "b_page: " + hex(self.b_page) + "\n"
		s += "b_blocknr: " + hex(self.b_blocknr) + "\n"
		s += "b_size: " + hex(self.b_size) + "\n"
		s += "b_data: " + hex(self.b_data) + "\n"

		for i in range(0,6):
			s += ("junk2["+str(i)+"]: " + hex(self.junk2[i]) + "\n")

		s += "b_count: " + hex(self.b_count) + "\n"

		return s

class dir_entry(Structure):
	_fields_ = [	('inode', c_uint),
			('rec_len', c_short),
			('name_len', c_byte),
			('file_type', c_byte)
		   ]

	def __init__(self, dm):
		self.dm = dm

	# Starting at the directory entry at address i,
	# search forward looking for a specific filename.
	def find_fname(self, addr, limit, basename):
		de = dir_entry(self.dm)

		i = addr
		while True:
			self.dm.read(de, i)
			if de.inode > 0:
				fname = self.dm.read_bytes(i+8, de.name_len)
				print fname
				if fname == basename:
					return i
				i += de.rec_len
				if i >= limit:
					break
			else:
				break
		return 0

	def remove(self, start, addr):
		de = dir_entry(self.dm)
		nxt = dir_entry(self.dm)

		i = start;
		while True:
			self.dm.read(de, i)
			if addr == (i + de.rec_len):
				self.dm.read(nxt, i+de.rec_len)
				de.rec_len += nxt.rec_len
				self.dm.write(de, i)
				break
			i += de.rec_len
