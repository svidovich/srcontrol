#!/usr/bin/env python3
import os

# Goals: Get the PID of the current process.
#        Read from a CGROUP.
#        Add the current process to a new CGROUP.
#        Verify that the process made it to the new CGROUP.

pid = os.getpid()
print(f'PID of this process is {pid}')

CGROUP_DIR_FILES = os.listdir('/sys/fs/cgroup')
print(CGROUP_DIR_FILES)

wait = input('Press enter to exit')
