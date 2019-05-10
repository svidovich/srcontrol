import cgroup

my_group = cgroup.Cgroup(group_name='my_group', hierarchies=['memory', 'cpu,cpuacct'])
try:
    print(my_group.constructed_subgroups)
    constructed_subgroup = '/sys/fs/cgroup/memory/my_group'
    metric_name = 'memory.usage_in_bytes'
    metric_type = 'key_value'

    usage_in_bytes = my_group.read_group_metric(constructed_subgroup=constructed_subgroup, metric_name=metric_name, metric_type=metric_type)
    print(f'Memory usage in bytes: {usage_in_bytes}')
finally:
    my_group.cleanup()