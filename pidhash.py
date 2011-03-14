from kstructs import *
from statichash import *

class PidHash(StaticHash):
	shift_name = "pidhash_shift"
	hash_root_name = "pid_hash"
	item = pid()
