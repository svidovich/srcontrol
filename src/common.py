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
            hierarchy_listing_dictionary['index'] = hierarchy_listing_split[0] 
            hierarchy_listing_dictionary['directory'] = hierarchy_listing_split[2]
            # TODO I need to figure out what this is really called
            # Also this might have to go :(
            hierarchy_name = hierarchy_listing_split[1] if hierarchy_listing_split[1] != '' else 'base'
            hierarchy_name = hierarchy_name.split('=')[1] if '=' in hierarchy_name else hierarchy_name
            spec[hierarchy_name] = hierarchy_listing_dictionary
        return spec

