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
