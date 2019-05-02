#!/usr/bin/env python3
import common
from pprint import pprint

# TODO: Implement testing with an actual fucking testing library

# Tests for load_hierarchies
h = common.load_hierarchies()
print(f'Sample hierarchy list:\n{h}')

# Tests for load_groups_and_files
gsf = common.load_groups_and_files()
print('Sample groups and files data:')
pprint(gsf)

# Tests for load_group_files

# Common usage
gf = common.load_group_files(group_name='test_group')
print('Sample group files data:')
pprint(gf)

# Raise ValueError
try:
    gf = common.load_group_files()
except Exception as e:
    print(e)

# Raise TypeError
try:
    gf = common.load_group_files(group_name=5)
except Exception as e:
    print(e)