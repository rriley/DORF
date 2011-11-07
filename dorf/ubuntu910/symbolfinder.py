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
