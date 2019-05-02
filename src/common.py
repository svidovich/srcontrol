#!/usr/bin/env python3
import os

CGROUP_BASE_DIR = '/sys/fs/cgroup'

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
def load_hierarchies(dir=CGROUP_BASE_DIR):
    cgls = os.listdir(dir)
    hierarchies = []
    for probable_hierarchy in cgls:
        full_hierarchy_path = os.path.join(dir, probable_hierarchy)
        if os.path.isdir(full_hierarchy_path) and not os.path.islink(full_hierarchy_path):
            hierarchies.append(probable_hierarchy)
    return hierarchies

# load_groups_and_files
# Inputs
# dir: string
# The top level cgroup directory
#
# Outputs
# groups_and_files: dict
# A large dictionary containing every cgroup currently
# on the system, its children, and all files in the group
def load_groups_and_files(dir=CGROUP_BASE_DIR):
    hierarchies = load_hierarchies()
    groups_and_files = []
    for hierarchy in hierarchies:
        hierarchy_base_path = os.path.join(CGROUP_BASE_DIR, hierarchy)
        for (root, dirs, files) in os.walk(hierarchy_base_path):
            group_and_files = {}
            group_and_files['group'] = root
            group_and_files['subgroups'] = dirs if dirs else None
            group_and_files['files'] = files if files else None
            groups_and_files.append(group_and_files)

    return groups_and_files

# load_group_files
# Inputs
# dir: string
# The top level cgroup directory
# group_name: string
# The name of the cgroup of interest.
#
# Outputs:
# files: dict
# A dictionary object whose keys are base hierarchies and
# whose values are the files contained under the group.
def load_group_files(dir=CGROUP_BASE_DIR, group_name=None):
    if group_name is None:
        raise ValueError('load_group_files: group_name not set.')
    if not isinstance(group_name, str):
        raise TypeError('load_group_files: group_name should be a string.')
    hierarchies = load_hierarchies()
    group_files = {}
    for hierarchy in hierarchies:
        hierarchy_base_path = os.path.join(CGROUP_BASE_DIR, hierarchy)
        for (root, dirs, files) in os.walk(hierarchy_base_path):
            if group_name in dirs:
                group_dir = os.path.join(root, group_name)
                print(f'group_dir: {group_dir}')
                files = [f for f in os.listdir(group_dir) if os.path.isfile(os.path.join(group_dir, f))]
                group_files[hierarchy] = files
    return group_files
