import common
import logging
import os
import sys
from metric import metric

# TODO: UNIT TESTS DAMMIT

# Instantiate logger
logging.basicConfig(level=logging.DEBUG, format='[%(levelname).8s] Function %(funcName).12s: %(message)s')
logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.INFO)

CGROUP_BASE_DIR = '/sys/fs/cgroup'

# TODO: Testing!
# TODO: Error handling around removal of groups. Will need to
# pull in the proof of concept code around this where we parse
# a process' original cgroups from /proc and put them back.
# TODO: Define function that allows us to add a routine to a
# cgroup.
class Cgroup(object):
    def __init__(self, group_name=None, hierarchies=None):
        self.hierarchies = hierarchies
        self.constructed_subgroups = []
        if group_name is None:
            raise ValueError('__init__: Expected value group_name is None.')
        if hierarchies is None:
            raise ValueError('__init__: Expected value hierarchies is None.')
        possible_hierarchies = common.load_hierarchies()
        # If there is no group name, we cannot create a group
        if group_name is None:
            raise ValueError('Cannot make cgroup without group name.')
        # If there {is,are} no hierarch{y,ies}, we cannot create a group
        if hierarchies is None:
            raise ValueError('Cannot make cgroup without hierarchies.')
        # We cannot create a group under a false hierarchy
        for hierarchy in hierarchies:
            if hierarchy not in possible_hierarchies:
                raise ValueError(f'Chosen hierarchy {hierarchy} is not an available system CGROUP hierarchy.')
        # If we are not root we will not have permission to create a group
        if os.geteuid() != 0:
            raise PrivilegeError(f'EUID is nonzero. It must be 0: Elevate the privilege of the program to continue.')
        # Make the new cgroup under each desired hierarchy.
        # Group name can also be a path into an already extant subgroup.
        logger.info('Constructing CGROUPS')
        for hierarchy in hierarchies:
            new_cgroup = os.path.join(CGROUP_BASE_DIR, hierarchy, group_name)
            try:
                os.mkdir(new_cgroup)
                self.constructed_subgroups.append(new_cgroup)
            except Exception:
                raise
    
    def execute_function_in_cgroup(self, *args, function=None):
        if function is None:
            raise ValueError('execute_function_in_cgroup: Expected argument function is None.')
        # Get pid to avoid double execution
        parent_pid = os.getpid()
        # Fork to a new process and get new pid
        os.fork()
        pid = os.getpid()
        return_value = None
        # os.wait()
        if pid != parent_pid:
            # Get the cgroup information for the new pid so that it can be returned later
            spec = common.parse_proc_cgroup_file(pid)
            # Add the process to the cgroup.procs file in each of the desired cgroups
            common.add_process_to_cgroup(subgroups=self.constructed_subgroups, pid=pid)
            # Execute the function under the cgroup and collect the return value
            return_value = function(args) if args else function()
            # Put the process back to the cgroup it was originally contained in
            common.return_process_to_original_cgroup(spec=spec, pid=pid)
            # Exit the fork.
            # Q: HOW DO I EXIT THE FORK BUT ALSO RETURN.
            # sys.exit()
            os._exit(0)
            # Return the value obtained from executing the function
        os.wait()
        return return_value

    # Don't get excited yet. This is just the header. I need to figure out how I want to do
    # the retry logic before I flesh this out.
    def execute_auto_restarting_function_in_cgroup(self, *args, function=None, retries=0):
        # Retry is based on whether or not I detect that a process was killed due to an OOM error.
        # As such, I need to be able to detect OOM errors.
        # Maybe this will change. ( Reading exit codes? )
        # https://stonesoupprogramming.com/2017/09/07/python-fork-exit-status/
        # I would like to be able to reprovision a function with more memory where possible
        # if it is truly killed due to ENOMEM. Thus, I will still probably need this even if I do
        # make it so that exit codes are read to see if the child succeeded or not.
        if not any('memory' in hierarchy for hierarchy in self.hierarchies):
            raise NotSupportedError('Auto restart is only supported for CGROUPS with the \'memory\' hierarchy.')
        if retries == 0:
            logger.warn('Using auto restarting function with 0 retries.')

    def read_group_metric(self, constructed_subgroup=None, metric_name=None):
        metric_types = ['key_value', 'multiline', 'chain']
        if constructed_subgroup is None:
            raise ValueError('read_group_metric: Expected value hierarchy is None.')
        if constructed_subgroup not in self.constructed_subgroups:
            raise ValueError('read_group_metric: Selected subgroup not in available subgroups.')
        if metric_name is None:
            raise ValueError('read_group_metric: Expected value metric_name is None.')

        with open(os.path.join(constructed_subgroup, metric_name), 'r') as file_handle:
            metric_type = metric.detect_metric_type(file_handle)
            if metric_type == 'key_value':
                return metric.parse_metric_key_value(cgroup_path=constructed_subgroup, metric_name=metric_name)
            if metric_type == 'multiline':
                return metric.parse_metric_pairs(cgroup_path=constructed_subgroup, metric_name=metric_name)
            if metric_type == 'chain':
                raise NotImplementedError

    def cleanup(self):
        logger.info(f'Removing CGROUPS')
        for constructed_subgroup in self.constructed_subgroups:
            try:
                os.rmdir(constructed_subgroup)
            except Exception:
                raise


class PrivilegeError(Exception):
    def __init__(self, message):
        super().__init__(message)

class NotSupportedError(Exception):
    def __init__(self, message):
        super().__init__(message)
