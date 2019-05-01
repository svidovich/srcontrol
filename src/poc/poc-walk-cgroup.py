#!/usr/bin/env python3
import sys
sys.path.append('..')
import os
import common

from pprint import pprint

#
# GOAL: Walk a cgroup and parse its child groups in a meaningful way DONE
#
# This proof of concept is a precursor to a lot of things -- this is how I can
# detect all of the various groups and subgroups on the system. It will be
# helpful later to be able to talk about a group's parents.
#
# The next use of this will be to extract relevant metrics. I will need to
# build parsers for all of the different metric file formats which exist
# in cgroups.
# 


CGROUP_BASE_DIR = '/sys/fs/cgroup'
hierarchies = common.load_hierarchies()

groups_and_files = []
for hierarchy in hierarchies:
    hierarchy_base_path = os.path.join(CGROUP_BASE_DIR, hierarchy)
    for (root, dirs, files) in os.walk(hierarchy_base_path):
        group_and_files = {}
        group_and_files['group'] = root
        group_and_files['subgroups'] = dirs if dirs else None
        group_and_files['files'] = files if files else None
        groups_and_files.append(group_and_files)

pprint(groups_and_files)