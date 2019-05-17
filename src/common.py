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
# A nested dictionary, the first layer being the hierarchies the process belongs to.
def parse_proc_cgroup_file(pid=None):
    if pid is None:
        raise ValueError('Expected argument pid is None.')
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
                hierarchy_listing_dictionary[
                    'index'] = hierarchy_listing_split[0]
                hierarchy_listing_dictionary[
                    'directory'] = hierarchy_listing_split[2]
                hierarchy_name = hierarchy_listing_split[1]
                hierarchy_name = hierarchy_name.split(
                    '=')[1] if '=' in hierarchy_name else hierarchy_name
                spec[hierarchy_name] = hierarchy_listing_dictionary
        return spec


# Could these next two functions be merged somehow?


# return_process_to_original_cgroup
# Inputs
# spec: dict
# The output of the function parse_proc_cgroup_file
# pid: int ( Should this be changed to int, str? )
# The pid of the process to be returned to its original group
#
# Ouputs
# void
#
# This function will read the spec obtained from a process' /proc/pid/cgroup
# file, and use that information to return it to its original group. This
# function must be called after a fork occurs, but before an exit.
def return_process_to_original_cgroup(spec, pid, dir=CGROUP_BASE_DIR):
    # Make sure we have the data we need.
    if not isinstance(pid, int):
        raise TypeError(
            f'Argument pid must be of type int; {type(pid)} was received.')
    if not isinstance(spec, dict):
        raise TypeError(
            f'Argument spec must be of type dict; {type(spec)} was received.')

    for hierarchy, mount_data in spec.items():
        mount_data['directory'] = mount_data['directory'].replace('/', '', 1)
        original_cgroup_path = os.path.join(dir, hierarchy,
                                            mount_data['directory'])
        original_cgroup_procs_file = os.path.join(original_cgroup_path,
                                                  'cgroup.procs')
        with open(original_cgroup_procs_file, 'a') as cgprocs:
            cgprocs.write(str(pid))


# add_process_to_cgroup
# Inputs
# subgroups: list
# subgroups is a list of strings containing absolute paths to the subgroups
# to which a process is to be added. An example could be
# ['/sys/fs/cgroup/memory/user.slice', '/sys/fs/cgroup/cpu,cpuacct']
# pid: string, int
# The pid of the process to be added to the subgroups in subgroups
# dir: string
# The top level cgroup directory
#
# Outputs
# void
def add_process_to_cgroup(subgroups, pid, dir=CGROUP_BASE_DIR):

    for subgroup in subgroups:
        if not dir in subgroup:
            raise ValueError(
                f'Subgroup {subgroup} is not an absolute path to a valid cgroup location.'
            )
    for subgroup in subgroups:
        # We assume that these are absolute paths.
        subgroup_procs_file = os.path.join(subgroup, 'cgroup.procs')
        with open(subgroup_procs_file, 'a') as procs_file:
            procs_file.write(str(pid))


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
        if os.path.isdir(full_hierarchy_path
                         ) and not os.path.islink(full_hierarchy_path):
            hierarchies.append(probable_hierarchy)
    return hierarchies


# load_groups_and_files
# Inputs
# dir: string
# The top level cgroup directory
#
# Outputs
# groups_and_files: list
# A large list containing dictionaries, themselves containing
# every cgroup currently on the system, its children,
# and all files in the groups.
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
def load_group_files(group_name, dir=CGROUP_BASE_DIR):
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
                files = [
                    f for f in os.listdir(group_dir)
                    if os.path.isfile(os.path.join(group_dir, f))
                ]
                group_files[hierarchy] = files
    return group_files
