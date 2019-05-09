import os
import unittest
import metric

CGROUP_BASE_DIR = '/sys/fs/cgroup'
class TestMetricParsers(unittest.TestCase):

    # Tests for None handling in parser functions

    def test_parse_metric_key_value_without_cgroup_path(self):
        with self.assertRaises(ValueError):
            _ = metric.parse_metric_key_value(metric_name='foo')

    def test_parse_metric_key_value_without_metric_name(self):
        with self.assertRaises(ValueError):
            memory_cgroup_path = os.path.join(CGROUP_BASE_DIR, 'memory')
            _ = metric.parse_metric_key_value(cgroup_path=memory_cgroup_path)
    
    def test_parse_metric_pairs_without_cgroup_path(self):
        with self.assertRaises(ValueError):
            _ = metric.parse_metric_pairs(metric_name='foo')

    def test_parse_metric_pairs_without_metric_name(self):
        with self.assertRaises(ValueError):
            memory_cgroup_path = os.path.join(CGROUP_BASE_DIR, 'memory')
            _ = metric.parse_metric_pairs(cgroup_path=memory_cgroup_path)

    # Tests for nonexistent paths

    def test_parse_metric_key_value_with_bad_path(self):
        bad_path = '/sys/fd/cgroup'
        bad_memory_cgroup_path = os.path.join(bad_path, 'memory')
        with self.assertRaises(FileNotFoundError):
            _ = metric.parse_metric_key_value(cgroup_path=bad_memory_cgroup_path, metric_name='memory.limit_in_bytes')

    def test_parse_metric_pairs_with_bad_path(self):
        bad_path = '/sys/fd/cgroup'
        bad_memory_cgroup_path = os.path.join(bad_path,'memory.limit_in_bytes')
        with self.assertRaises(FileNotFoundError):
            _ = metric.parse_metric_pairs(cgroup_path=bad_memory_cgroup_path, metric_name='memory.stat')

    # Tests for good inputs

    def test_parse_metric_key_value_with_good_inputs(self):
        memory_cgroup_path = os.path.join(CGROUP_BASE_DIR, 'memory')
        test_metric_name = 'memory.limit_in_bytes'
        output = metric.parse_metric_key_value(cgroup_path=memory_cgroup_path, metric_name=test_metric_name)
        self.assertIsInstance(output, str)

    def test_parse_metric_pairs_with_good_inputs(self):
        memory_cgroup_path = os.path.join(CGROUP_BASE_DIR, 'memory')
        test_metric_name = 'memory.stat'
        output = metric.parse_metric_pairs(cgroup_path=memory_cgroup_path, metric_name=test_metric_name)
        self.assertIsInstance(output, dict)