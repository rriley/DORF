from statichash import *

import version
exec("from dorf."+version.my_version+".kstructs import *")

class PidHash(StaticHash):
	shift_name = "pidhash_shift"
	hash_root_name = "pid_hash"
	item = pid()
