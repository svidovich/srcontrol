import sys
sys.path.append('..')
import common
import pprint

# Goals: Read the CGROUP spec for pid 1                         DONE
#        Parse the CGROUP spec for pid 1 in a meaningful way    DONE
#
# Sample Output:
#
# {'base': {'directory': '/init.scope', 'index': '0'},
#  'blkio': {'directory': '/', 'index': '3'},
#  'cpu,cpuacct': {'directory': '/', 'index': '8'},
#  'cpuset': {'directory': '/', 'index': '4'},
#  'devices': {'directory': '/init.scope', 'index': '10'},
#  'freezer': {'directory': '/', 'index': '11'},
#  'hugetlb': {'directory': '/', 'index': '9'},
#  'memory': {'directory': '/init.scope', 'index': '6'},
#  'name=systemd': {'directory': '/init.scope', 'index': '1'},
#  'net_cls,net_prio': {'directory': '/', 'index': '5'},
#  'perf_event': {'directory': '/', 'index': '12'},
#  'pids': {'directory': '/init.scope', 'index': '7'},
#  'rdma': {'directory': '/', 'index': '2'}}
#
# This can be dumped to valid JSON or pickled easily.

pid_1_cgroup_spec = common.parse_proc_cgroup_file(1)


pprint.pprint(pid_1_cgroup_spec)