#!/usr/bin/env python3
import os

# parse_proc_cgroup_file
# Inputs
# pid: int, str
# The pid of the process whose cgroup file is to be parsed
#
# Outputs
# spec: dict
# A nested dictionary, the first layer being the hierarchies the process belongs to
def parse_proc_cgroup_file(pid):
    # If you don't have the /proc filesystem mounted you're a chump
    with open(f'/proc/{pid}/cgroup', 'r') as proc_cgroup_file:
        # This comes with newlines attached. Fix that in place.
        pid_cgroup_spec = [x.strip() for x in proc_cgroup_file.readlines()]
        spec = {}
        for hierarchy_listing in pid_cgroup_spec:
            hierarchy_listing_dictionary = {}
            hierarchy_listing_split = hierarchy_listing.split(':')
            # In this case, I'm choosing to index the data by hierarchy name
            # This will make it easy to look through later
            if hierarchy_listing_split[0] != '0':
                hierarchy_listing_dictionary['index'] = hierarchy_listing_split[0]
                hierarchy_listing_dictionary['directory'] = hierarchy_listing_split[2]
                hierarchy_name = hierarchy_listing_split[1]
                hierarchy_name = hierarchy_name.split('=')[1] if '=' in hierarchy_name else hierarchy_name
                spec[hierarchy_name] = hierarchy_listing_dictionary
        return spec

# load_hierarchies
# Inputs
# dir: string
# The top level cgroup directory
#
# Outputs
# hierarchies: list
# A list containing the available cgroup hierarchies
#
# If the cgroup top level is mounted somewhere other than
# at /sys/fs/cgroup, it can be specified
def load_hierarchies(dir='/sys/fs/cgroup'):
    cgls = os.listdir(dir)
    hierarchies = []
    for probable_hierarchy in cgls:
        full_hierarchy_path = os.path.join(dir, probable_hierarchy)
        if os.path.isdir(full_hierarchy_path) and not os.path.islink(full_hierarchy_path):
            hierarchies.append(probable_hierarchy)
    return hierarchies