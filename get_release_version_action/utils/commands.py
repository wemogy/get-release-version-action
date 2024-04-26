"""Utilities for running commands."""
import logging
import os
import subprocess
from collections.abc import Sequence
from typing import TypeAlias

logger = logging.getLogger('wemogy.get-release-version-action')

__all__ = [
    'run_command'
]

StringOrPath: TypeAlias = str | os.PathLike[str]


def log_command(
        command: Sequence[StringOrPath],
        process: subprocess.CompletedProcess[str] | subprocess.CalledProcessError,
        env: dict[str, StringOrPath] | None = None
) -> None:
    """Log the command, environment and process result."""
    return_code = process.returncode
    command_str = ' '.join([f'"{x}"' if (' ' in str(x) or str(x) == '') else str(x) for x in command])
    env_str = ('\nEnvironment: ' + '; '.join([f'${k}="{v}"' for k, v in env.items()])) if env is not None else ''
    output = '\n' + process.stdout if process.stdout.strip() else ''

    if isinstance(process, subprocess.CalledProcessError):
        logger.error(
            'Process exited unsuccessful with exit code %s:\nCommand: %s%s%s',
            return_code, command_str, env_str, output
        )
    else:
        logger.debug(
            'Process exited successful with exit code %s:\nCommand: %s%s%s',
            return_code, command_str, env_str, output
        )


def run_command(*command: StringOrPath) -> str:
    """
    Run the given command and return the output if the command was successful,
    else log the output and raise an exception.

    :param command: The command to run.
    :returns: The command's output if the command exited successful.
    :raises subprocess.CalledProcessError: If the command did not exit successful.
    """
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as exc:
        log_command(command, exc)
        raise exc

    log_command(command, process)
    return process.stdout
