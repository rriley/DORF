from kstructs import *

"""
This class is meant to handle Static Hash tables.
Don't create one directly, it is meant to be inherited from.
(To handle types, etc.)

item should be an object type that has...
	-a __str__ function that works
	-list_offset defined as the number of bytes from the start
	 of the structure until the start of the list
	-a next() method that returns the address of the next item
	 in the list
	-a compare(thing) method that returns 0 if the thing is the same
	 as the object, + if its "greater" and - if its "less".
"""
class StaticHash:
	shift_name = "unused"
	hash_root_name = "unused"
	item = object()

	def __init__(self, sf, dm):
		self.sf = sf
		self.dm = dm
		self.shift = dm.read_int(sf.find(self.shift_name))
		self.hashroot = dm.read_int(sf.find(self.hash_root_name))
		print hex(self.hashroot)

	def print_all(self):
		for i in range(0, 1 << self.shift):
			tptr = self.dm.read_int(self.hashroot+4*i)
			while tptr != 0:
				self.dm.read(self.item,tptr-self.item.list_offset)
				print self.item
				tptr = self.item.next();

	def find(self, thing):
                for i in range(0, 1 << self.shift):
                        tptr = self.dm.read_int(self.hashroot+4*i)
                        while tptr != 0:
                                self.dm.read(self.item,tptr-self.item.list_offset)
				if self.item.compare(thing) == 0:
					return self.item
                                tptr = self.item.next();
		return None
