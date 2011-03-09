import os, sys
from ctypes import *

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

class task_struct(Structure):
	_fields_ = [ 	('junk1',c_char * 456), 
			('next_task',c_void_p), 
			('prev_tast',c_void_p),
			('junk2',c_char * 56),
			('pid', c_int)
		   ]
