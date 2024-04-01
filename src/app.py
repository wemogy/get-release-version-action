"""
A GitHub Action to determine the next version by checking the commit history
for Conventional Commits with support for hotfix changes.
"""
import logging
import logging.config
import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import git
import yaml
from semantic_release import LevelBump, ParseError
from semantic_release.commit_parser import AngularCommitParser, AngularParserOptions
from semver import Version

logger = logging.getLogger('wemogy.get-release-version-action')


def parse_bool(string: str) -> bool:
    """Parse a string into a boolean."""
    return string.lower() == 'true'


def nullable_string(string: str) -> str | None:
    """Return None if the string is empty or only contains whitespace characters."""
    if string.strip() == '' or string == 'NONE':
        return None
    return string


def print_github_actions_output() -> None:
    """Print the contents of the GITHUB_OUTPUT file."""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    # noinspection PyBroadException
    try:
        with open(file_path, 'r') as fh:
            content = fh.read()
            logger.debug('Content of GITHUB_OUTPUT file "%s":\n%s', file_path, content)
    except Exception:
        # Catching every exception since this function is not necessary for the script to run
        logger.warning('An exception was ignored while trying to get contents of GITHUB_OUTPUT file', exc_info=True)


def clear_github_output() -> None:
    """Clear the GITHUB_OUTPUT file."""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    logging.info('Clearing GITHUB_OUTPUT file "%s"', file_path)

    with open(file_path, 'w') as fh:
        fh.write('')


def set_github_output(name: str, value: Any) -> None:
    """Set the key-value-pair as a GitHub actions output"""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    with open(file_path, 'a') as fh:
        fh.write(f'{name}={value}\n')


def setup_logging(debug: bool = False) -> None:
    """Setup logging"""
    config_file = Path(__file__).resolve().parent / 'logging.config.yaml'

    with config_file.open('r') as config_stream:
        config = yaml.load(config_stream, yaml.SafeLoader)

    if debug:
        config['handlers']['stdout']['formatter'] = 'indent'
        config['handlers']['stdout']['level'] = 'DEBUG'

    logging.config.dictConfig(config)
    logging.getLogger().setLevel(logging.DEBUG)


def run_command(*command: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> str:
    """
    Run the given command and return the output if the command was successful,
    else log the output and raise an exception.

    :param command: The command to run
    :returns: The command's output if the command exited successful
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


def get_current_version_tag(repo: git.Repo, prefix: str, suffix: str | None) -> git.TagReference | None:
    """
    Get the current version (= the latest git tag).
    If there are no tags, return None.
    """
    # Reverse the list of tags to start with the most recent one
    for tag in sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True):
        # Check if the tag name starts with the specified prefix
        if tag.name.startswith(prefix) and (suffix is None or suffix in tag.name):
            logger.debug('Found tag %s (%s)', tag.name, tag.commit.hexsha)
            return tag

    logger.debug('Found no tags that have the prefix %s', prefix)
    return None


def get_new_commits(repo: git.Repo, starting_tag: git.TagReference | None) -> list[git.Commit]:
    """Get all commits newer than the current_version tag."""
    max_commits = 50
    commit_offset = 0
    reached_starting_tag = False
    new_commits: list[git.Commit] = []

    while not reached_starting_tag:
        commits = repo.iter_commits(max_count=max_commits, skip=commit_offset)
        i = 0

        for commit in commits:
            i += 1

            if starting_tag is None:
                logger.debug('Commit %s was found', commit.hexsha)
                new_commits.append(commit)
                continue

            if commit == starting_tag.commit:
                logger.debug(
                    'Commit %s is current version %s (%s)',
                    commit.hexsha, starting_tag.name, starting_tag.commit.hexsha
                )
                reached_starting_tag = True
                break

            logger.debug(
                'Commit %s is newer than current version %s (%s)',
                commit.hexsha, starting_tag.name, starting_tag.commit.hexsha
            )
            new_commits.append(commit)

        commit_offset += max_commits

        if i < max_commits:
            logger.debug('Reached end of commit history')
            break

    return new_commits


def get_next_version(repo: git.Repo, current_version_tag: git.TagReference | None,
                     current_version: str) -> tuple[str, bool]:
    """Determine the next version."""
    # 1. Add all commits to list until commit with current_version_tag reached
    new_commits = get_new_commits(repo, current_version_tag)

    # 2. Apply conventional commits to list
    commit_parser = AngularCommitParser(AngularParserOptions())
    parsing_results = [commit_parser.parse(commit) for commit in new_commits]

    # 3. Check if list contains major (=> bump major), minor or patch
    # Reduce the parsing results to an integer: 0 = chore / unknown, 1 = patch, 2 = minor, 3 = major
    commit_bumps = [
        0 if isinstance(result, ParseError) else
        3 if result.bump == LevelBump.MAJOR else
        2 if result.bump == LevelBump.MINOR else
        1 if result.bump == LevelBump.PATCH else
        0
        for result in parsing_results
    ]

    # The maximum of the numbers in commit_bumps is the version we need to bump
    version_to_bump = max(commit_bumps) if len(commit_bumps) > 0 else 0
    logger.debug('Version to bump is %s (0 = chore / unknown, 1 = patch, 2 = minor, 3 = major)', version_to_bump)

    # 4. Bump the version
    current_version_obj = Version.parse(current_version)

    if version_to_bump == 1:
        return str(current_version_obj.bump_patch()), True
    if version_to_bump == 2:
        return str(current_version_obj.bump_minor()), True
    if version_to_bump == 3:
        return str(current_version_obj.bump_major()), True

    return current_version, False


def increment_suffix(version: str, suffix: str) -> str:
    """Increment the version suffix (-{suffix}.) or append -{suffix}.1, if the suffix does not exist."""
    return str(Version.parse(version).bump_prerelease(suffix))


def create_tag(version: str) -> None:
    """Create a new git tag for the given version and push it if a remote is configured."""
    logger.info('Creating tag %s', version)

    # Create the tag
    run_command('git', 'tag', version)

    git_remote = run_command('git', 'remote', 'show')

    if git_remote == '':
        logger.info('No remote found, skipping pushing')
        return

    run_command('git', 'push', 'origin', version)

    logger.info('Pushed tag %s to remote', version)


def get_new_version(
        prefix: str,
        previous_version_suffix: str | None,
        bumping_suffix: str,
        only_bump_suffix: bool
) -> tuple[str, str, bool]:
    """
    Get the new version, involving the only_increase_suffix flag.

    :returns: A tuple of the previous version, the next version and if any changes were detected.
    """
    repo = git.Repo(os.getcwd())
    current_version_tag = get_current_version_tag(repo, prefix, previous_version_suffix)

    if current_version_tag is None:
        current_version = '0.0.0'
    else:
        current_version = current_version_tag.name.removeprefix(prefix)
        if previous_version_suffix is not None:
            current_version = current_version.replace(f'-{previous_version_suffix}', '', 1)

    next_version, has_changes = get_next_version(repo, current_version_tag, current_version)

    logger.debug(
        'current_version=%s, next_version=%s, has_changes=%s',
        current_version, next_version, has_changes
    )

    # Example case: No change that requires a semantic version increase
    if not has_changes:
        logger.info('No changes detected, version stays the same.')
        return current_version, next_version, has_changes

    # Example case: Hotfix
    if only_bump_suffix:
        logger.info('Only the suffix will be incremented.')
        return current_version, increment_suffix(current_version, bumping_suffix), has_changes

    # Example case: New Release
    logger.info('Semantic Version will be incremented.')
    return current_version, next_version, has_changes


def main() -> None:
    """
    A GitHub Action to determine the next version by checking the commit history
    for Conventional Commits with support for hotfix changes.
    """
    # region argparse
    parser = ArgumentParser(
        description='A GitHub Action to determine the next version by checking the commit history for Conventional '
                    'Commits with support for hotfix changes.',
        allow_abbrev=False
    )

    parser.add_argument(
        '-v', '--verbose',
        dest='verbose_output',
        action='store_true',
        help='Print debug messages to stdout.'
    )

    parser.add_argument(
        '--prefix',
        dest='prefix',
        type=str,
        required=False,
        default='v',
        help='The prefix that should be prepended to the version.'
    )

    parser.add_argument(
        '--suffix',
        dest='suffix',
        type=nullable_string,
        required=False,
        default='NONE',
        help='The suffix that should be appended to the version (e.g. `beta`).'
    )

    parser.add_argument(
        '--previous-version-suffix',
        dest='previous_version_suffix',
        type=nullable_string,
        required=False,
        default='NONE',
        help='The suffix that should be replaced with the value in `suffix`.'
    )

    parser.add_argument(
        '--bumping-suffix',
        dest='bumping_suffix',
        type=str,
        required=False,
        default='hotfix',
        help='The suffix to append to the version (or increment if it already exists) if `only-bump-suffix` is `true`.'
    )

    parser.add_argument(
        '--only-bump-suffix',
        dest='only_bump_suffix',
        type=parse_bool,
        required=False,
        default='false',
        help='Bump the `bumping-suffix` instead of the version if changes were detected.'
    )

    parser.add_argument(
        '--create-tag',
        dest='create_tag',
        type=parse_bool,
        required=False,
        default='true',
        help='Create a git tag for the version and push it if a remote is configured.'
    )

    args = parser.parse_args()
    setup_logging(args.verbose_output)
    # endregion

    previous_version, new_version, has_changes = get_new_version(
        args.prefix,
        args.previous_version_suffix,
        args.bumping_suffix,
        args.only_bump_suffix
    )

    if args.previous_version_suffix is not None:
        if '-' in previous_version:
            previous_version = previous_version.replace('-', f'-{args.previous_version_suffix}-', 1)
        else:
            previous_version += f'-{args.previous_version_suffix}'

    if args.suffix is not None:
        if '-' in new_version:
            new_version = new_version.replace('-', f'-{args.suffix}-', 1)
        else:
            new_version += f'-{args.suffix}'

    new_version_tag_name = f'{args.prefix}{new_version}'
    previous_version_tag_name = f'{args.prefix}{previous_version}'

    if args.create_tag and has_changes:
        create_tag(new_version_tag_name)

    # clear the output to ensure that it is empty
    clear_github_output()

    set_github_output('version', new_version)
    set_github_output('version-name', new_version_tag_name)
    set_github_output('previous-version', previous_version)
    set_github_output('previous-version-name', previous_version_tag_name)
    set_github_output('has-changes', str(has_changes).lower())

    print_github_actions_output()

    logger.info('Version is %s', new_version)


if __name__ == '__main__':
    main()
