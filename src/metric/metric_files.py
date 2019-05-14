# TODO: Add data for all of the various possible hierarchies that
# allows us to detect which files are settings and which are metrics

general_metrics_files = [
    'cgroup.procs',
    'cgroup.sane_behavior',
    'tasks'
]

# cpu,cpuacct

cpu_metrics_files = [
    'cpu.cfs_period_us',
    'cpu.shares',
    'cpu.stat'
]

cpuaccount_metrics_files = [
    'cpuacct.stat',
    'cpuacct.usage_all',
    'cpuacct.usage_percpu_sys',
    'cpuacct.usage_percpu_user',
    'cpuacct.usage_percpu',
    'cpuacct.usage_sys',
    'cpuacct.usage_user',
    'cpuacct.usage'
]

# memory

memory_metrics_files = [
    'memory.failcnt',
    'memory.limit_in_bytes',
    'memory.max_usage_in_bytes',
    'memory.move_charge_at_immigrate',
    'memory.numa_stat',
    'memory.oom_control',
    'memory.pressure_level',
    'memory.soft_limit_in_bytes',
    'memory.stat',
    'memory.swappiness',
    'memory.usage_in_bytes'
]

kmem_metrics_files = [
    'memory.kmem.failcnt',
    'memory.kmem.limit_in_bytes',
    'memory.kmem.max_usage_in_bytes',
    'memory.kmem.slabinfo',
    'memory.kmem.tcp.failcnt',
    'memory.kmem.tcp.limit_in_bytes',
    'memory.kmem.tcp.max_usage_in_bytes',
    'memory.kmem.tcp.usage_in_bytes',
    'memory.kmem.usage_in_bytes'
]

memsw_metrics_files = [
    'memory.memsw.failcnt',
    'memory.memsw.limit_in_bytes',
    'memory.memsw.max_usage_in_bytes',
    'memory.memsw.usage_in_bytes'
]