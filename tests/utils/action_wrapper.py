"""Wrapper for the get-release-version-action script."""
from __future__ import annotations

import dataclasses
import logging
import os
import subprocess
import sys
from os import PathLike
from collections.abc import Sequence
from dataclasses import dataclass
from inspect import get_annotations
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess
from typing import Any

logger = logging.getLogger('wemogy.get-release-version-action.tests.wrapper')

__all__ = [
    'ActionInputs',
    'ActionOutputs',
    'run_action'
]


@dataclass(frozen=True, kw_only=True)
class ActionInputs:
    """Inputs of the get-release-version-action."""

    prefix: str = 'v'
    """The prefix that should be prepended to the version."""

    suffix: str = ''
    """The suffix that should be appended to the version (e.g. `beta`)."""

    previous_version_suffix: str = ''
    """The suffix that should be replaced with the value in `suffix` (e.g. `dev`)."""

    bumping_suffix: str = 'hotfix'
    """The suffix to append to the version (or increment if it already exists) if `only_bump_suffix` is `true`."""

    only_bump_suffix: bool = False
    """Bump the `bumping_suffix` instead of the version if changes were detected."""

    create_tag: bool = True
    """Create a git tag for the version and push it if a remote is configured."""

    def to_arg_list(self) -> list[str]:
        """Convert the arguments object into a list of command line arguments."""
        arg_list: list[str] = []

        for name, value in dataclasses.asdict(self).items():
            arg_list.append('--' + name.replace('_', '-'))
            arg_list.append(str(value).lower() if isinstance(value, bool) else str(value))

        return arg_list


@dataclass(frozen=True, kw_only=True)
class ActionOutputs:
    """Outputs of the get-release-version-action."""
    version: str
    """The next version, without the prefix."""

    version_name: str
    """The next version, with the prefix."""

    previous_version: str
    """The previous version, without the prefix."""

    previous_version_name: str
    """The previous version, with the prefix."""

    tag_created: bool
    """If any relevant changes got detected."""

    @classmethod
    def from_github_output(cls, github_output_file: Path) -> ActionOutputs:
        """
        Parse the GitHub actions output into an outputs object.

        :param github_output_file: The path to the file provided to the script
                                   via the GITHUB_OUTPUT environment variable.
        """
        lines = github_output_file.read_text(encoding='utf-8').splitlines()
        ctor_args: dict[str, Any] = {}

        for line in lines:
            raw_name, raw_value = line.strip().split('=', 1)
            name = raw_name.replace('-', '_')

            field_type = get_annotations(cls, eval_str=True)[name]
            value: Any

            if field_type is bool:
                value = raw_value.lower() == 'true'
            elif field_type is str:
                value = raw_value
            else:
                value = field_type(raw_value)

            ctor_args[name] = value

        return cls(**ctor_args)  # pylint: disable=missing-kwoa


def log_command(
        command: Sequence[str | PathLike[str]],
        env: dict[str, str | PathLike[str]],
        process: CompletedProcess[str] | CalledProcessError
) -> None:
    """Log the command, environment and process result."""
    return_code = process.returncode
    command_str = ' '.join([f'"{x}"' if (' ' in str(x) or str(x) == '') else str(x) for x in command])
    env_str = '; '.join([f'${k}="{v}"' for k, v in env.items()])
    output = '\n' + process.stdout if process.stdout.strip() else ''

    if isinstance(process, CalledProcessError):
        logger.error(
            'Process exited unsuccessful with exit code %s:\nCommand: %s\nEnvironment: %s%s',
            return_code, command_str, env_str, output
        )
    else:
        logger.info(
            'Process exited successful with exit code %s:\nCommand: %s\nEnvironment: %s%s',
            return_code, command_str, env_str, output
        )


def run_action(
        inputs: ActionInputs,
        script_path: Path | None = None
) -> ActionOutputs:
    """
    Run the get-release-version-action script with the current interpreter.

    :param inputs: The action inputs.
    :param script_path: The path to the get-release-version-action script. Defaults to ``__file__/../../../src/app.py``.
    :returns: The parsed action output.
    :raises CalledProcessError:
    """
    github_output_file = Path('github-output.txt')

    command: tuple[str | PathLike[str], ...] = (
        sys.executable,
        script_path if script_path is not None else Path(__file__).resolve().parent.parent.parent / 'src' / 'app.py',
        *inputs.to_arg_list(),
        '--verbose'
    )

    env: dict[str, str | PathLike[str]] = {
        'GITHUB_OUTPUT': github_output_file,
        'PATH': os.environ['PATH']
    }

    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            text=True,
            env=env
        )
    except CalledProcessError as e:
        log_command(command, env, e)
        raise e

    log_command(command, env, process)
    return ActionOutputs.from_github_output(github_output_file)
