DORF: Data-Only Rootkit Framework
====
This is the source code related to the paper
"A framework for prototyping and testing data-only rootkit attacks"

Quick and Dirty Instructions to Get Started
----
* Install OpenSUSE 11.4 into a VM.  Make sure your machine is running kernel 2.6.37.1-1.2  (It should be.)
* Install git and then clone the code down.
* Edit version.py and change my_version to "opensuse114"
* Use the attack-prochide.py script to try and hide a process based on the PID.

Notes
----
* Most Linux distros require a kernel recompile to enable /dev/mem.
OpenSUSE didn't, hence why I used for the quick and dirty above.
* Any changes to the kernel version (even on the same distro) may
require altering the offsets in dorf/<distro>/kstructs.py.  There is
a kernel module in kmodule/ that can help you find the correct offsets.
Load it into the kernel and then check your syslog for the output.
