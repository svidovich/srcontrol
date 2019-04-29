#!/usr/bin/env python3

# Goals: Run functions in different processes from the top level script DONE
#        Return a value from a forked function TECHNICALLY DONE

import os
import sys

def run_in_separate_process(func, *args):
    arguments = args
    os.fork()
    return_value = func(arguments)

    sys.exit()
    return return_value

def function_one(args):
    f1_pid = os.getpid()
    parent_pid = os.getppid()
    print(f'function_one running with pid {f1_pid} with parent pid {parent_pid}')
    return 5

def function_two(args):
    f2_pid = os.getpid()
    parent_pid = os.getppid()
    print(f'function_two running with pid {f2_pid} with parent pid {parent_pid}')

# When running the second function in a new process, its parent
# will be the process which was running the first process.
# I don't know if that matters. I should talk to Warren.
def main():
    process_output = run_in_separate_process(function_one)
    print(process_output)
    process_output = run_in_separate_process(function_two)
    print(process_output)

if __name__ == "__main__":
    main()