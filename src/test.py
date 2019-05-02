#!/usr/bin/env python3
import common
import unittest
from unittest import mock
from pprint import pprint

# TODO: Implement testing with an actual fucking testing library

# I wonder how easy it will be to make this pass on
# any given machine -- how will different machines
# differ in the cgroups they contain?
class TestCommonFunctions(unittest.TestCase):

    ###### Tests for load_hierarchies
    def test_load_hierarchies(self):
        h = common.load_hierarchies()
        hierarchies_test_data = ['hugetlb', 'cpuset', 'perf_event', 'memory', 'devices', 'net_cls,net_prio', 'blkio', 'pids', 'freezer', 'cpu,cpuacct', 'rdma', 'systemd', 'unified']
        self.assertEqual(h, hierarchies_test_data)

    ###### Tests for load_groups_and_files
    @mock.patch('common.load_hierarchies')
    def test_load_groups_and_files(self, lh_mock):
        gsf = common.load_groups_and_files()
        lh_mock.assert_called_once()
        self.assertIsInstance(gsf, list)


    ###### Tests for load_group_files

    # This will require more instrumentation as
    # I will need to make a sample group in code
    # # Common usage
    # gf = common.load_group_files(group_name='test_group')
    # print('Sample group files data:')
    # pprint(gf)

    # # Raise ValueError
    # try:
    #     gf = common.load_group_files()
    # except Exception as e:
    #     print(e)

    # # Raise TypeError
    # try:
    #     gf = common.load_group_files(group_name=5)
    # except Exception as e:
    #     print(e)