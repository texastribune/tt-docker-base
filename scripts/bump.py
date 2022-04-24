
#!/usr/bin/env python3

import re
from enum import Enum
import sys
import os
import subprocess

VERSION_FILE_PATH = './VERSION'


class Increment(Enum):
    major = '1'
    minor = '2'
    patch = '3'


def execute_command(command):
    """
    Execute a shell command and stream the output until the process completes.

    Args:
        command (str): The command to execute.

    Returns:
        None
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        encoding='utf-8',
        errors='replace'
    )
    while True:
        realtime_output = process.stdout.readline()
        if realtime_output == '' and process.poll() is not None:
            break
        if realtime_output:
            print(realtime_output.strip(), flush=True)


def yes_or_no(question):
    """
    Asks user a yes/no question.

    Args:
        question (str): Question to ask

    Returns:
        bool: True if user answers yes, False otherwise
    """
    reply = str(input(f"{question} (y/n): ")).lower().strip()
    no_reply_msg = "Please enter"
    if not reply:
        return yes_or_no(no_reply_msg)
    elif reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    else:
        return yes_or_no(no_reply_msg)


def check_valid_version(version):
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def validate_increment(increment):
    valid_increments = [x.value for x in Increment]
    if increment not in valid_increments:
        valid_increments_str = ', '.join(valid_increments)
        print("Invalid value '{}'. must be one of: {}".format(
            increment, valid_increments_str))
        sys.exit(1)


def get_current_version():
    with open(VERSION_FILE_PATH, 'r') as f:
        version = f.read().strip()
        if not check_valid_version(version):
            error_msg = "Invalid version: {}. Must be of format X.Y.Z".format(
                version)
            raise ValueError(error_msg)
        return version


def generate_new_version(current_version, increment):
    # generate new version
    new_version = None
    version_parts = current_version.split('.')
    if increment == Increment.patch.value:
        new_patch = int(version_parts[2]) + 1
        new_version = '.'.join(
            [version_parts[0], version_parts[1], str(new_patch)])
    elif increment == Increment.minor.value:
        new_minor = int(version_parts[1]) + 1
        new_version = '.'.join([version_parts[0], str(new_minor), '0'])
    elif increment == Increment.major.value:
        new_major = int(version_parts[0]) + 1
        new_version = '.'.join([str(new_major), '0', '0'])
    return new_version


def write_version_file(new_version):
    with open(VERSION_FILE_PATH, 'w') as f:
        f.write(new_version)


def main():
    current_version = get_current_version()
    print("Current version: {}".format(current_version))
    prompt = "Bump major (1), minor (2), or patch (3)?"
    increment = input(f"{prompt}: ").lower().strip()
    validate_increment(increment)
    new_version = generate_new_version(current_version, increment)
    confirm_q = "Bump {} to {} and commit?".format(
        VERSION_FILE_PATH, new_version)
    confirm_reply = yes_or_no(confirm_q)
    if confirm_reply == False:
        print("Exiting...")
        sys.exit(0)
    write_version_file(new_version)
    cmd_gitadd = f"git add {VERSION_FILE_PATH}"
    execute_command(cmd_gitadd)
    cmd_commit = "git commit -m 'bump version to {}'".format(new_version)
    execute_command(cmd_commit)


if __name__ == "__main__":
    main()
