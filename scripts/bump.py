
#!/usr/bin/env python3

import re
from enum import Enum
import sys
import os

VERSION_FILE_PATH = './VERSION'


class Increment(Enum):
    major = 1
    minor = 2
    patch = 3


def check_valid_version(version):
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def bump_version(increment):
    """
    Increments the version number in the VERSION file.

    Args:
        increment (str): One of "patch", "minor", "major"

    Returns:
        None
    """

    # validate args
    if not hasattr(Increment, increment):
        valid_increments = ', '.join(
            [increment.name for increment in Increment])
        raise ValueError("Invalid increment '{}'. Must be one of: {}".format(
            increment, valid_increments))

    # read VERSION file
    with open(VERSION_FILE_PATH, 'r') as f:
        current_version = f.read().strip()
        if not check_valid_version(current_version):
            error_msg = "Invalid version: {}. Must be of format X.Y.Z".format(
                current_version)
            raise ValueError(error_msg)

    # generate new version
    new_version = None
    version_parts = current_version.split('.')
    if increment == Increment.patch.name:
        new_patch = int(version_parts[2]) + 1
        new_version = '.'.join(
            [version_parts[0], version_parts[1], str(new_patch)])
    elif increment == Increment.minor.name:
        new_minor = int(version_parts[1]) + 1
        new_version = '.'.join([version_parts[0], str(new_minor), '0'])
    elif increment == Increment.major.name:
        new_major = int(version_parts[0]) + 1
        new_version = '.'.join([str(new_major), '0', '0'])

    # write
    with open(VERSION_FILE_PATH, 'w') as f:
        f.write(new_version)
    print("Version bumped: {} -> {}".format(current_version, new_version))


def main():
    if len(sys.argv) != 2:
        file_name = os.path.basename(__file__)
        print("Usage: {} <increment>".format(file_name))
        print("  increment: one of 'patch', 'minor', 'major'")
        sys.exit(1)
    bump_version(sys.argv[1])


if __name__ == "__main__":
    main()
