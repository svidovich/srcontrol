#!/usr/bin/env python3
import common
from pprint import pprint

h = common.load_hierarchies()
print(f'Sample hierarchy list:\n{h}')
gf = common.load_groups_and_files()
print('Sample groups and files data:')
pprint(gf)

