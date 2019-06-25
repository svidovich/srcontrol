import os

CGROUP_BASE_DIR = '/sys/fs/cgroup'


# yapf: disable
def adjust_blkio_tunable(blkio_group_path, tunable_parameter, lad_number, value):
    if value < 0:
        raise ValueError(f'Cannot ajust {tunable parameter} to non-natural number.')
    tunable_file = os.path.join(blkio_group_path, tunable_parameter)
    adjustment_string = f'{lad_number} {value}'
    with open(tunable_file, 'w') as file_handle:
        file_handle.write(adjustment_string)
# yapf: enable


class LimitExceededException(Exception):
    def __init__(self, message):
        super().__init__(message)
