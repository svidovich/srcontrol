import common
import logging
import os
import sys

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
    constructed_subgroups = []
    def __init__(self, group_name=None, hierarchies=None):
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
            self.constructed_subgroups.append(new_cgroup)
            os.mkdir(new_cgroup)
    
    def execute_function_in_cgroup(self, *args, function=None):
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
            # os._exit(0)
            # Return the value obtained from executing the function
            return return_value
        os.wait()

    def cleanup(self):
        logger.info(f'Removing CGROUPS')
        for constructed_subgroup in self.constructed_subgroups:
            os.rmdir(constructed_subgroup)


class PrivilegeError(Exception):
    def __init__(self, message):
        super().__init__(message)
