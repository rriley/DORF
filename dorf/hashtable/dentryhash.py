from statichash import *

import version
exec("from dorf."+version.my_version+".kstructs import *")

class DentryHash(StaticHash):
	shift_name = "d_hash_shift"
	hash_root_name = "dentry_hashtable"
	item = dentry()

	def __init__(self, sf, dm):
		self.item.set_dm(dm)
		StaticHash.__init__(self, sf, dm)
