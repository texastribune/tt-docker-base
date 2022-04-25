#!/usr/bin/env python3

import re
from enum import Enum
import sys
import subprocess
from pathlib import Path


VERSION_FILE_PATH = './VERSION'


class Increment(Enum):
    major = '1'
    minor = '2'
    patch = '3'


class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def wrap(text, color):
    return f"{color}{text}{bc.ENDC}"


def execute_command(command):
    """
    Execute a shell command and stream the output until the process completes.

    Args:
        command (str): The command to execute.

    Returns:
        Exit code of the command.
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
    exit_code = process.wait()
    return exit_code


def get_active_branch_name():

    head_dir = Path(".") / ".git" / "HEAD"
    with head_dir.open("r") as f:
        content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]


def check_exit_code(exit_code):
    if exit_code != 0:
        print(f"Error: exit code {exit_code}")
        sys.exit(exit_code)


def yes_or_no(question):
    """
    Asks user a yes/no question.

    Args:
        question (str): Question to ask

    Returns:
        bool: True if user answers yes, False otherwise
    """
    reply = str(
        input(f"{question} ({wrap('y/n', bc.BOLD)}): ")).lower().strip()
    no_reply_msg = "Please enter"
    if not reply:
        return yes_or_no(no_reply_msg)
    elif reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    else:
        return yes_or_no(no_reply_msg)


def exit_without_error():
    print("Exiting")
    sys.exit(0)


def check_valid_version(version):
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def validate_increment(increment):
    valid_increments = [x.value for x in Increment]
    if increment not in valid_increments:
        valid_increments_str = ', '.join(valid_increments)
        print(
            f"Invalid value '{increment}'. must be one of: {valid_increments_str}")
        sys.exit(1)


def get_current_version():
    with open(VERSION_FILE_PATH, 'r') as f:
        version = f.read().strip()
        if not check_valid_version(version):
            error_msg = f"Invalid version: {version}. Must be of format X.Y.Z"
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
    # check branch
    active_branch = get_active_branch_name()
    if active_branch != "master":
        print(
            f"{wrap('WARNING',bc.WARNING)}: You are on branch '{active_branch}'.\nIt's generally recommended you run this script on master after first merging your feature branch.")
        reply_switch = yes_or_no("Change to master and pull?")
        if reply_switch is True:
            exit_code_exit_code = execute_command(
                "git checkout master && git pull origin master")
            check_exit_code(exit_code_exit_code)
            active_branch = get_active_branch_name()

    # get current version
    current_version = get_current_version()
    print(
        f"Current tt-docker-base version on '{active_branch}': {current_version}")

    # get desired bump
    q_increment = f"Bump major ({wrap('1', bc.BOLD)}), minor ({wrap('2', bc.BOLD)}), or patch ({wrap('3', bc.BOLD)})?"
    reply_increment = input(f"{q_increment}: ").lower().strip()
    validate_increment(reply_increment)
    new_version = generate_new_version(current_version, reply_increment)

    # save and commit
    q_commit = f"Bump version to {wrap(new_version,bc.UNDERLINE)} and commit?"
    confirm_commit = yes_or_no(q_commit)
    if confirm_commit == False:
        exit_without_error()
    print(f"{VERSION_FILE_PATH} file changed: {current_version} -> {wrap(new_version,bc.UNDERLINE)}")
    write_version_file(new_version)
    cmd_gitadd = f"git add {VERSION_FILE_PATH}"
    exit_code_gitadd = execute_command(cmd_gitadd)
    check_exit_code(exit_code_gitadd)
    cmd_commit = f"git commit -m 'bump version to {new_version}'"
    exit_code_commit = execute_command(cmd_commit)
    check_exit_code(exit_code_commit)

    # tag and push
    q_tag = f"Tag commit as {wrap(new_version,bc.UNDERLINE)} and push local '{active_branch}' to remote '{active_branch}'?"
    confirm_tag = yes_or_no(q_tag)
    if confirm_tag == False:
        exit_without_error()
    cmd_tag = f'git tag {new_version}'
    exit_code_tag = execute_command(cmd_tag)
    check_exit_code(exit_code_tag)
    cmd_push_active = f'git push origin {active_branch}'
    exit_code_push = execute_command(cmd_push_active)
    check_exit_code(exit_code_push)


if __name__ == "__main__":
    main()
