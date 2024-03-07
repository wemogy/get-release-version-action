import logging
import logging.config
import os
import re
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import git
import semver
import yaml

logger = logging.getLogger('wemogy.get-release-version-action')

def print_github_output():
    file_path = os.environ['GITHUB_OUTPUT']
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            logger.info(f"Content of file '{file_path}':\n{content}")
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def clear_output() -> None:
    """
    Clear the GitHub actions output file
    """
    if not os.environ.get('GITHUB_OUTPUT'):
        logging.info('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    output_file_path = os.environ['GITHUB_OUTPUT']
    logging.info('Clearing GitHub actions output file: %s', output_file_path)
    
    # Open the file in write mode to clear its contents
    with open(output_file_path, 'w') as fh:
        fh.truncate(0)

def set_output(name: str, value: Any) -> None:
    """
    Set the key-value-pair as a GitHub actions output

    :param name: The name of the output
    :param value: The value of the output
    """
    if not os.environ.get('GITHUB_OUTPUT'):
        logger.info('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        # write new line
        print(f'{name}={value}', file=fh)


def setup_logging() -> None:
    """Setup logging"""
    config_file = Path(__file__).resolve().parent / 'logging.config.yaml'

    with config_file.open('r') as config_stream:
        config = yaml.load(config_stream, yaml.SafeLoader)

    logging.config.dictConfig(config)
    logging.getLogger().setLevel(logging.DEBUG)


def run_command(*command: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> str:
    """
    Run the given command and return the output if the command was successful,
    else log the output and raise an exception.

    :param command: The command to run
    :return: The command's output if the command exited successful
    :throws subprocess.CalledProcessError: If the command did not exit successful.
    """
    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(
            'Process %s exited unsuccessful with exit code %s:\n%s',
            ' '.join([str(x) for x in command]), e.returncode, e.stdout
        )
        raise e

    logger.debug(
        'Process %s exited successful with exit code %s:\n%s',
        ' '.join([str(x) for x in command]), process.returncode, process.stdout
    )
    return process.stdout


def get_current_version_tag() -> str:
    """
    Get the current version (= the latest git tag).
    If there are no tags, return 0.0.0

    :return: The current version
    """
    repo = git.Repo(os.getcwd())

    if len(repo.tags) == 0:
        return '0.0.0'

    return repo.tags[-1].name


def get_next_version(prefix: str) -> str:
    """
    Determine the next version.

    :return: The next version
    """

    config_path = Path(__file__).resolve().parent / 'semantic-release.config.json'

    # replace {{PREFIX}} with the actual prefix
    with open(config_path, 'r') as file:
        config = file.read()
        config = config.replace('{{PREFIX}}', prefix)

    with open(config_path, 'w') as file:
        file.write(config)

    output = run_command(
        'semantic-release',
        '-vv',  # Enable debug output
        '--config', Path(__file__).resolve().parent / 'semantic-release.config.json',
        'version',
        '--print',  # Print the version to the command line
        '--skip-build',  # Don't build the app (done in a separate action)
        '--no-commit',  # Don't commit build artifacts or other changes by semantic-release
                        # (because there shouldn't be any)
        '--no-tag',  # Don't create a git tag
                     # (we create it manually because semantic-releases tag feature doesn't work for some reason)
        '--no-changelog',  # Don't update the changelog file
        '--no-push',  # Don't push any changes (because there shouldn't be any)
        '--no-vcs-release',  # Don't create a GitHub release (done in a separate action)
    )

    version_pattern = re.compile(r'^\d+\.\d+\.\d+$', re.MULTILINE)
    next_version = version_pattern.search(output).group()
    return next_version


def increment_hotfix(version: str, hotfix_suffix: str) -> str:
    """
    Increment the hotfix version (-h.) or append -h.1, if the suffix does not exist.

    :param version: The old version
    :param hotfix_suffix: The suffix that should be used for the hotfix number
    :return: The new version
    """
    return semver.bump_prerelease(version, hotfix_suffix)


def create_tag(version: str) -> None:
    """
    Create a new git tag for the given version and push it if a remote is configured.

    :param version: The version that the tag should be named
    """
    logger.info('Creating tag %s', version)

    # Create the tag
    run_command('git', 'tag', version)

    git_remote = run_command('git', 'remote', 'show')

    if git_remote == '':
        logger.info('No remote found, skipping pushing')
        return

    run_command('git', 'push', 'origin', version)

    logger.info('Pushed tag %s to remote', version)


def main() -> None:
    """Increment the hotfix version if needed."""
    setup_logging()

    # region argparse
    parser = ArgumentParser(
        description='Increment the hotfix version if needed.',
        allow_abbrev=False
    )

    parser.add_argument(
        '--prefix',
        dest='prefix',
        type=str,
        default='v',
        help='The prefix that should be prepended to the version.'
    )

    parser.add_argument(
        '--suffix',
        dest='suffix',
        type=str,
        help='The suffix that should be incremented.'
    )

    parser.add_argument(
        '--only-increase-suffix',
        dest='only_increase_suffix',
        type=str,
        default='False',
        help='Only increases the suffix increment if any change got detected.'
    )

    parser.add_argument(
        '--create-tag',
        dest='create_tag',
        type=str,
        default='False',
        help='Create a Git Tag for the version and push it if a remote is configured.'
    )

    args = parser.parse_args()
    args.only_increase_suffix = args.only_increase_suffix.lower() == 'true'
    args.create_tag = args.create_tag.lower() == 'true'
    # endregion

    current_version_tag = get_current_version_tag()
    current_version = current_version_tag[len(args.prefix):] # remove the prefix
    next_version = get_next_version(args.prefix)
    has_changes = next_version != current_version

    logger.debug(
        'current_version=%s, next_version=%s, has_changes=%s',
        current_version, next_version, has_changes
    )

    if has_changes:
        logger.info('Changes detected, next version is %s', next_version)

        if args.only_increase_suffix:
            # Example case: Hotfix
            logger.info('Only the suffix will be incremented.')
            new_version = increment_hotfix(current_version, args.suffix)
        else:
            # Example case: New Release
            logger.info('Semantic Version will be incremented.')
            new_version = next_version
    else:
        # Example case: No change that requires a semantic version increase
        logger.info('No changes detected, version stays the same.')
        new_version = next_version

    new_version_tag = f'{args.prefix}{new_version}'

    if args.create_tag and has_changes:
        create_tag(new_version_tag)

    # clear the output to ensure that it is empty
    clear_output()

    set_output('version', new_version)
    set_output('version-name', new_version_tag)
    set_output('has-changes', str(has_changes).lower())

    print_github_output()

    logger.info('Version is %s', new_version)

if __name__ == '__main__':
    main()
