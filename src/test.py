#!/usr/bin/env python3
import common
import cgroup
import unittest
from unittest import mock
from pprint import pprint

# TODO: Implement testing with an actual fucking testing library


class TestCgroup(unittest.TestCase):

    # Test case: hierarchy is not valid.
    def test_with_bad_hierarchy(self):
        with self.assertRaises(ValueError):
            _ = cgroup.Cgroup(group_name='new_group',
                              hierarchies=['memory', 'fake-hierarchy'])

    # Test case: script has nonzero euid.
    def test_as_nonroot(self):
        with self.assertRaises(cgroup.PrivilegeError):
            _ = cgroup.Cgroup(group_name='new_group',
                              hierarchies=['memory', 'cpu,cpuacct'])


# I wonder how easy it will be to make this pass on
# any given machine -- how will different machines
# differ in the cgroups they contain?
class TestCommonFunctions(unittest.TestCase):

    ###### Tests for load_hierarchies
    def test_load_hierarchies(self):
        h = common.load_hierarchies()
        hierarchies_test_data = [
            'hugetlb', 'cpuset', 'perf_event', 'memory', 'devices',
            'net_cls,net_prio', 'blkio', 'pids', 'freezer', 'cpu,cpuacct',
            'rdma', 'systemd', 'unified'
        ].sort()
        self.assertEqual(h.sort(), hierarchies_test_data)

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

    # Test case: Bad typing in group name
    def test_load_group_files_bad_group(self):
        with self.assertRaises(TypeError):
            _ = common.load_group_files(group_name=5)
