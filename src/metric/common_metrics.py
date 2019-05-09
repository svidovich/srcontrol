# These metrics are ones that a developer might commonly desire.
# These are baked for your delight. If there is something that you'd like to
# see that isn't here, please make an issue or make a PR and I would gladly review it.
#
# Since these are common, they only gather metrics of cgroups that commonly exist.
# These will not work for your custom groups; you will have to write your own functions
# for those. Behold, in the future code will exist to help construct such functions.

import os
import math
import metric

CGROUP_BASE_DIR='/sys/fs/cgroup'
def return_cpu_usage_in_seconds_k_significant_digits(k=3):
    cpu_cgroup_dir = os.path.join(CGROUP_BASE_DIR, 'cpu,cpuacct')
    metric_name = 'cpuacct.usage'
    cpu_usage_as_int = int(metric.parse_metric_key_value(cgroup_path=cpu_cgroup_dir, metric_name=metric_name))
    cpu_usage = cpu_usage_as_int / math.pow(10, 9)
    return round(cpu_usage, k)

