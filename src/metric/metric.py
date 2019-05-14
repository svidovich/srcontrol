# According to the redhat guide, there are three types of metrics:
#
# Value metrics: Just a value in a file DONE
#
# Key-Value paired metrics: Metrics of the form
# key1 value1
# ...
# keyK valueK
# ...
# keyN valueN
#
# DONE
#
# And chain types, which are a whole fucked up mess of their own
# TODO: Add chain types parser once I find a chain type metric
# TODO: Autodetection of metric types.

import os

CGROUP_BASE_DIR = '/sys/fs/cgroup'

# parse_metric_key_value
# Inputs
# cgroup_path: str
# The path to the cgroup containing the metric of interest
# metric_name: str
# The name of the file containing the metric of interest
#
# Outputs
# metric_value: str
# The metric retrieved from a file. Until I'm convinced otherwise, these
# files may contain strings OR ints OR floats. As such, the developer MUST
# cast them as such after return.
#
# This function is used to parse those files for which the filename is the 
# key representing the metric, and the contents the value of the metric.

def parse_metric_key_value(cgroup_path=None, metric_name=None):
    if cgroup_path is None:
        raise ValueError('parse_metric_key_value: Expected input cgroup path is None.')
    if metric_name is None:
        raise ValueError('parse_metric_key_value: Expected input metric_name is None.')
    metric_file_path = os.path.join(cgroup_path, metric_name)
    with open(metric_file_path, 'r') as metric_file:
        # Strip, otherwise we may receive a newline
        metric_value = metric_file.read().strip()
        return metric_value

# parse_metric_pairs
# Inputs
# cgroup_path: str
# The path to the cgroup containing the metric of interest
# metric_name: str
# The name of the file containing the metric of interest
#
# Outputs
# metric_dictionary: dict
# A dictionary containing key-value pairs representing 'sub-metrics'
# underneath the main metric
#
# This function is used to parse those files for which the filename represents
# the overall metric, but the contents are several key-value pairs representative
# of the various parts of the overall metric.

def parse_metric_pairs(cgroup_path=None, metric_name=None):
    if cgroup_path is None:
        raise ValueError('parse_metric_key_value: Expected input cgroup path is None.')
    if metric_name is None:
        raise ValueError('parse_metric_key_value: Expected input metric_name is None.')
    metric_dictionary = {}
    metric_file_path = os.path.join(cgroup_path, metric_name)
    with open(metric_file_path, 'r') as metric_file:
        for line in metric_file:
            # These 'sub-metrics' come in key value pairs like
            # keyK valueK
            # As such, split on the spaces. The first item in the
            # resultant list will be the key, the second the value.
            metric_key_value_list = line.split(' ')
            metric_key = metric_key_value_list[0]
            # Strip, otherwise we may recieve a newline
            metric_value = metric_key_value_list[1].strip()
            metric_dictionary[metric_key] = metric_value
    return metric_dictionary


def detect_metric_type(file_handle):
    lines = [line.strip() for line in file_handle.readlines()]
    if len(lines) == 1:
        return 'key_value'
    if len(lines) > 1:
        if not any(len(line.split()) > 2 for line in lines):
            return 'multiline'
        else:
            return 'chain'
