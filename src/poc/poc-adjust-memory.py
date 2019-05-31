#!/usr/bin/env python3

# GOAL: Make a memory cgroup. Adjust its memory cap by writing
# to memory.limit_in_bytes. DONE

import os
import sys
sys.path.append('..')
from cgroup import Cgroup

mygroup = Cgroup(group_name='test_group', hierarchies=['memory'])

try:
    memory_subgroup_path = mygroup.constructed_subgroups[0]
    limit_in_bytes_path = os.path.join(memory_subgroup_path,
                                       'memory.limit_in_bytes')
    _ = input('press enter to write to file')
    with open(limit_in_bytes_path, 'w') as limit_in_bytes_file_handle:
        limit_in_bytes_file_handle.write('100000')
    _ = input('waiting')
finally:
    mygroup.cleanup()