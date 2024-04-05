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

    logger.info('Clearing GITHUB_OUTPUT file "%s"', file_path)

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


def get_current_version_tag(repo: git.Repo, prefix: str, suffix: str | None, bumping_suffix: str) -> git.TagReference | None:
    """
    Get the current version (= the latest git tag).
    If there are no tags, return None.
    """
    # Reverse the list of tags to start with the most recent one
    for tag in sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True):
        # Check if the tag name starts with the specified prefix and,
        # if the suffix is not None, if the suffix is in the tag name,
        # else check if no suffix other than the bumping suffix is in the tag name.
        if tag.name.startswith(prefix) and \
            (suffix is None or suffix in tag.name) and \
                (suffix is not None or '-' not in tag.name.replace(f'-{bumping_suffix}', '')):
            logger.debug('Found tag %s (%s) with prefix "%s" and suffix "%s"',
                         tag.name, tag.commit.hexsha, prefix, suffix)
            return tag

    logger.debug('Found no tags that have the prefix "%s" and suffix "%s"', prefix, suffix)
    return None


def build_hash_based_tag_name(prefix: str, commit: git.Commit, suffix: str | None) -> str:
    """Build a hash based tag name."""
    # This is slicing the hexsha string to get the first 7 characters.
    # Git often abbreviates hashes to the first 7 characters, as this is usually enough to uniquely identify a commit.
    return prefix + commit.hexsha[:7] + (f'-{suffix}' if suffix is not None else '')


def get_current_version_hash(repo: git.Repo, prefix: str, suffix: str | None) -> str | None:
    """
    Get the current version (= the latest git tag).
    If there are no tags, return None.
    """
    # Reverse the list of tags to start with the most recent one
    for tag in sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True):
        # Create a hash based tag name
        hash_based_tag = build_hash_based_tag_name(prefix, tag.commit, suffix)
        # Check if the tag name starts with the specified prefix
        if tag.name == hash_based_tag:
            logger.debug('Found tag %s (%s)', tag.name, tag.commit.hexsha[:7])
            return tag.commit.hexsha[:7]

    logger.debug('Found no tags that have the prefix %s', prefix)
    return None


def get_new_commits(repo: git.Repo, starting_tag: git.TagReference | None) -> list[git.Commit]:
    """Get all commits newer than the current_version tag."""
    max_commits = 50
    commit_offset = 0
    reached_starting_tag = False
    new_commits: list[git.Commit] = []

    while not reached_starting_tag:
        try:
            commits = repo.iter_commits(max_count=max_commits, skip=commit_offset)
        except ValueError:
            logger.warning('No commits found')
            return []

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
                     current_version: str | None) -> tuple[str, bool]:
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
    current_version_obj = Version.parse(current_version or '0.0.0')

    if version_to_bump == 1:
        return str(current_version_obj.bump_patch()), True
    if version_to_bump == 2:
        return str(current_version_obj.bump_minor()), True
    if version_to_bump == 3:
        return str(current_version_obj.bump_major()), True

    return current_version or '0.0.0', False


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
        suffix: str | None,
        previous_version_suffix: str | None,
        bumping_suffix: str,
        only_bump_suffix: bool
) -> tuple[str | None, str, bool]:
    """
    Get the new version, involving the only_increase_suffix flag.

    :returns: A tuple of the previous version, the next version and if any changes were detected.
    """
    repo = git.Repo(os.getcwd())
    # Previous version is the latest version that was made, possibly on another branch / channel.
    # It is used to get the next version.
    previous_version_tag = get_current_version_tag(repo, prefix, previous_version_suffix, bumping_suffix)

    # Current version is the latest version on this branch / channel.
    # This is the version returned as previous version at the end of the script.
    current_version_tag = get_current_version_tag(repo, prefix, suffix, bumping_suffix)

    if previous_version_tag is None:
        previous_version: str | None = None
    else:
        previous_version = previous_version_tag.name.removeprefix(prefix)
        if previous_version_suffix is not None:
            previous_version = previous_version.replace(f'-{previous_version_suffix}', '', 1)

    if current_version_tag is None:
        current_version: str | None = None
    else:
        current_version = current_version_tag.name.removeprefix(prefix)
        if previous_version_suffix is not None:
            current_version = current_version.replace(f'-{suffix}', '', 1)

    next_version, has_changes = get_next_version(repo, previous_version_tag, previous_version)

    logger.debug(
        'current_version=%s, next_version=%s, has_changes=%s',
        previous_version, next_version, has_changes
    )

    # Example case: No change that requires a semantic version increase
    if not has_changes:
        logger.info('No changes detected, version stays the same.')
        return current_version, next_version, has_changes

    # Example case: Hotfix
    if only_bump_suffix:
        logger.info('Only the suffix will be incremented.')
        return current_version, increment_suffix(previous_version, bumping_suffix), has_changes

    # Example case: New Release
    logger.info('Semantic Version will be incremented.')
    return current_version, next_version, has_changes


def get_new_version_hash_based(
        prefix: str,
        previous_version_suffix: str | None
) -> tuple[str, str, bool]:
    """
    Get the new version based on the hash of the latest commit.

    :returns: A tuple of the previous version, the next version and if any changes were detected.
    """
    repo = git.Repo(os.getcwd())
    current_version = get_current_version_hash(repo, prefix, previous_version_suffix)
    next_version = repo.head.commit.hexsha[:7]
    has_changes = current_version != next_version

    logger.debug(
        'current_version=%s, next_version=%s, has_changes=%s',
        current_version, next_version, has_changes
    )

    # Example case: No change that requires a semantic version increase
    if not has_changes:
        logger.info('No changes detected, version stays the same.')
        return current_version, next_version, has_changes

    # Example case: New Release
    logger.info('Hash based version will be incremented.')
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

    parser.add_argument(
        '--mode',
        dest='mode',
        type=str,
        choices=('semantic', 'hash-based'),
        required=False,
        default='semantic',
        help='The mode to use for determining the next version. Possible values: `semantic`, `hash-based`.'
    )

    args = parser.parse_args()
    setup_logging(args.verbose_output)
    # endregion

    if args.mode == 'hash-based':
        previous_version, new_version, has_changes = get_new_version_hash_based(
            args.prefix,
            args.previous_version_suffix
        )
    else:
        previous_version, new_version, has_changes = get_new_version(
            args.prefix,
            args.suffix,
            args.previous_version_suffix,
            args.bumping_suffix,
            args.only_bump_suffix
        )

    if args.previous_version_suffix is not None and previous_version is not None:
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
    previous_version_tag_name = f'{args.prefix}{previous_version}' if previous_version else ''

    if args.create_tag and (has_changes or (previous_version != new_version)):
        create_tag(new_version_tag_name)

    # clear the output to ensure that it is empty
    clear_github_output()

    set_github_output('version', new_version)
    set_github_output('version-name', new_version_tag_name)
    set_github_output('previous-version', previous_version or '')
    set_github_output('previous-version-name', previous_version_tag_name)
    set_github_output('has-changes', str(has_changes).lower())

    print_github_actions_output()

    logger.info('Version is %s', new_version)


if __name__ == '__main__':
    main()
