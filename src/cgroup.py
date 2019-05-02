import common

class Cgroup(object):
    def __init__(self, group_name=None, hierarchies=None):
        possible_hierarchies = common.load_hierarchies()
        if group_name is None:
            raise ValueError('Cannot make cgroup without group name.')
        if hierarchies is None:
            raise ValueError('Cannot make cgroup without hierarchies.')
        for hierarchy in hierarchies:
            if hierarchy not in possible_hierarchies:
                raise ValueError(f'Chosen hierarchy {hierarchy} is not an available system CGROUP hierarchy.')