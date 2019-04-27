#!/usr/bin/env python3
import os
import sys
sys.path.append('..')
import common

# Goals: Get the PID of the current process.                 DONE
#        Read from a CGROUP.                                 DONE
#        Add the current process to a new CGROUP.            DONE
#        Verify that the process made it to the new CGROUP.  DONE
#        Remove the CGROUP.                                  DONE

# We need to run with privilege. Since this
# is linux, let's >>>check our privilege, and if 
# necessary run as root.
# We use execvp because it will not spin a child
# process, but rather use the current process.

if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
pid = os.getpid()
print(f'PID of this process is {pid}')
spec = common.parse_proc_cgroup_file(pid)
print(f'Cgroup spec for pid {pid}: \n{spec}')

CGROUP_DIR_FILES = os.listdir('/sys/fs/cgroup')
print(CGROUP_DIR_FILES)
if 'cpu' in CGROUP_DIR_FILES:
    print('Found cpu group. Changing directories.')
    os.chdir('/sys/fs/cgroup/cpu')
    print('Reading processes from cgroup.procs...')
    with open('cgroup.procs', 'r') as procs:
        # uncomment to see output from goal II
        # print(procs.read())
        pass
    print('Adding new cgroup underneath cpu...')
    os.mkdir('test_group')
    print('Changing directory to test_group...')
    if 'test_group' in os.listdir():
        os.chdir('test_group')
        print('Adding current process to cgroup...')
        with open('cgroup.procs', 'a+') as procs:
            procs.write(str(pid))
        exitbutton = input('Press enter to remove cgroup and exit')
        for hierarchy, mount_data in spec.items():
            mount_data['directory'] = mount_data['directory'].replace('/', '', 1)
            original_cgroup_path = os.path.join('/sys/fs/cgroup', hierarchy, mount_data['directory'])
            original_cgroup_procs_file = os.path.join(original_cgroup_path, 'cgroup.procs')
            with open(original_cgroup_procs_file, 'a') as cgprocs:
                cgprocs.write(str(pid))
        os.chdir('..')
        os.rmdir('test_group')
    else:
        print('Test group not found. Exiting, no action taken.')
    
