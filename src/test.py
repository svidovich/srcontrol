#!/usr/bin/env python3
import common
from pprint import pprint

h = common.load_hierarchies()
print(f'Sample hierarchy list:\n{h}')
gsf = common.load_groups_and_files()
print('Sample groups and files data:')
pprint(gsf)
gf = common.load_group_files(group_name='test_group')
print('Sample group files data:')
pprint(gf)
