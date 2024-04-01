import os
import subprocess
import logging
import dataclasses
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger('wemogy.get-release-version-action.tests.wrapper')


@dataclass(frozen=True, kw_only=True)
class ActionArguments:
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
        arg_list: list[str] = []

        for name, value in dataclasses.asdict(self).items():
            arg_list.append('--' + name.replace('_', '-'))
            arg_list.append(str(value).lower() if isinstance(value, bool) else str(value))

        return arg_list


@dataclass(frozen=True, kw_only=True)
class ActionOutputs:
    version: str
    """The next version, without the prefix."""

    version_name: str
    """The next version, with the prefix."""

    previous_version: str
    """The previous version, without the prefix."""

    previous_version_name: str
    """The previous version, with the prefix."""

    has_changes: bool
    """If any relevant changes got detected."""

    @classmethod
    def from_github_output(cls, github_output_file: Path):
        lines = github_output_file.read_text().splitlines()
        ctor_args: dict[str, Any] = {}

        for line in lines:
            raw_name, raw_value = line.strip().split('=', 1)
            name = raw_name.replace('-', '_')

            field_type = cls.__annotations__[name]

            if field_type is bool:
                value = raw_value.lower() == 'true'
            elif field_type is str:
                value = raw_value
            else:
                value = field_type(raw_value)

            ctor_args[name] = value

        return cls(**ctor_args)


def run_action(args: ActionArguments, python_executable: Path = None, python_path: Path = None, script_path: Path = None) -> ActionOutputs:
    python_executable = python_executable or Path(sys.executable)
    python_path = python_path or python_executable.parent
    script_path = script_path or Path(__file__).parent.parent.parent / 'src' / 'app.py'
    github_output_file = Path('github-output.txt')
    command = (python_executable, script_path, *args.to_arg_list(), '--verbose')
    env = {
        'GITHUB_OUTPUT': github_output_file,
        'PATH': os.getenv('PATH') + os.pathsep + str(python_path)
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
    except subprocess.CalledProcessError as e:
        logger.error(
            'Process exited unsuccessful with exit code %s:\nCommand: %s\nEnv: %s\n%s',
            e.returncode, ' '.join([str(x) for x in command]), env, e.stdout
        )
        raise e

    logger.debug(
        'Process exited successful with exit code %s:\nCommand: %s\nEnv: %s\n%s',
        process.returncode, ' '.join([str(x) for x in command]), env, process.stdout
    )

    return ActionOutputs.from_github_output(github_output_file)
