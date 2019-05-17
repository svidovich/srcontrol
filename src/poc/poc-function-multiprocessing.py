#!/usr/bin/env python3
import multiprocessing

# Goals:
# Run a function in a new process, and get its return value back to the parent.
# The function cannot take queue as an argument.

import os
import sys


def run_in_separate_process(func, *args):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=wrapper, args=(func, q, args))
    p.start()
    return_value = q.get()
    p.join
    return return_value


def wrapper(function, queue, *args):
    return_value = function(args)
    queue.put(return_value)


def function_one(args):
    f1_pid = os.getpid()
    parent_pid = os.getppid()
    print(
        f'function_one running with pid {f1_pid} with parent pid {parent_pid}')
    return 5


def function_two(args):
    f2_pid = os.getpid()
    parent_pid = os.getppid()
    print(
        f'function_two running with pid {f2_pid} with parent pid {parent_pid}')


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