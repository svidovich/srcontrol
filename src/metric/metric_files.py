# TODO: Add data for all of the various possible hierarchies that
# allows us to detect which files are settings and which are metrics

general_metrics_files = [
    'cgroup.procs',
    'cgroup.sane_behavior'
    'tasks',
]

cpu_metrics_files = [
    'cpu.cfs_period_us'
    'cpu.shares',
    'cpu.stat',
]

cpuaccount_metrics_files = [
    'cpuacct.stat',
    'cpuacct.usage_all',
    'cpuacct.usage_percpu_sys'
    'cpuacct.usage_percpu_user',
    'cpuacct.usage_percpu',
    'cpuacct.usage_sys',
    'cpuacct.usage_user',
    'cpuacct.usage',
]

