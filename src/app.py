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
import semver
import yaml
from semantic_release import LevelBump, ParseError
from semantic_release.commit_parser import AngularCommitParser, AngularParserOptions

logger = logging.getLogger('wemogy.get-release-version-action')


def print_github_actions_output() -> None:
    """Print the contents of the GITHUB_OUTPUT file."""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.info('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    # noinspection PyBroadException
    try:
        with open(file_path, 'r') as fh:
            content = fh.read()
            logger.debug('Content of GITHUB_OUTPUT file "%s":\n%s', file_path, content)
    except Exception:
        # Catching every exception since this function is not necessary for the script to run
        logger.exception('An error occurred')


def clear_github_output() -> None:
    """Clear the GITHUB_OUTPUT file."""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.info('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    logging.info('Clearing GITHUB_OUTPUT file "%s"', file_path)

    with open(file_path, 'w') as fh:
        fh.write('')


def set_github_output(name: str, value: Any) -> None:
    """Set the key-value-pair as a GitHub actions output"""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.info('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    with open(file_path, 'a') as fh:
        fh.write(f'{name}={value}\n')


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


def get_current_version_tag(repo: git.Repo, prefix: str) -> git.TagReference | None:
    """
    Get the current version (= the latest git tag).
    If there are no tags, return None.
    """
    try:
        # Reverse the list of tags to start with the most recent one
        for tag in reversed(repo.tags):
            # Check if the tag name starts with the specified prefix
            if tag.name.startswith(prefix):
                return tag
    except IndexError:
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

    # 4. Bump the version
    current_version_obj = semver.Version.parse(current_version)

    if version_to_bump == 1:
        return str(current_version_obj.bump_patch()), True
    if version_to_bump == 2:
        return str(current_version_obj.bump_minor()), True
    if version_to_bump == 3:
        return str(current_version_obj.bump_major()), True

    return current_version, False


def increment_suffix(version: str, suffix: str) -> str:
    """Increment the version suffix (-{suffix}.) or append -{suffix}.1, if the suffix does not exist."""
    return str(semver.Version.parse(version).bump_prerelease(suffix))


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
        suffix: str,
        only_increase_suffix: bool,
        only_replace_prefix_with: str | None
) -> tuple[str, bool]:
    """Get the new version, involving the only_increase_suffix flag."""
    repo = git.Repo(os.getcwd())
    current_version_tag = get_current_version_tag(repo, prefix)

    if current_version_tag is None:
        current_version = '0.0.0'
    else:
        current_version = current_version_tag.name.removeprefix(prefix)

    if only_replace_prefix_with is None:
        next_version, has_changes = get_next_version(repo, current_version_tag, current_version)
    else:
        # Only replace the suffix if
        if current_version.endswith(f'-{suffix}'):
            next_version = current_version.removesuffix(suffix) + only_replace_prefix_with
        else:
            next_version = current_version
        has_changes = False

    logger.info(
        'current_version=%s, next_version=%s, has_changes=%s',
        current_version, next_version, has_changes
    )

    # Example case: No change that requires a semantic version increase
    if not has_changes:
        logger.info('No changes detected, version stays the same.')
        return next_version, has_changes

    # Example case: Hotfix
    if only_increase_suffix:
        logger.info('Only the suffix will be incremented.')
        return increment_suffix(current_version, suffix), has_changes

    # Example case: New Release
    logger.info('Semantic Version will be incremented.')
    return next_version, has_changes


def main() -> None:
    """
    A GitHub Action to determine the next version by checking the commit history
    for Conventional Commits with support for hotfix changes.
    """
    setup_logging()

    # region argparse
    parser = ArgumentParser(
        description='A GitHub Action to determine the next version by checking the commit history for Conventional '
                    'Commits with support for hotfix changes.',
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
        default='hotfix',
        help='The suffix that should be incremented / appended to the version.'
    )

    parser.add_argument(
        '--only-increase-suffix',
        dest='only_increase_suffix',
        type=str,
        default='False',
        help='Increment the suffix if any changes got detected.'
    )

    parser.add_argument(
        '--only-replace-suffix-with',
        dest='only_replace_suffix_with',
        type=str,
        default='false',
        help="Don't increment the version, only replace the suffix in `suffix` with the suffix from this input. "
             "`create-tag` and `prefix` still work with this option."
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
    args.only_replace_suffix_with = args.only_replace_suffix_with.strip() or None
    # endregion

    new_version, has_changes = get_new_version(
        args.prefix,
        args.suffix,
        args.only_increase_suffix,
        args.only_replace_suffix_with
    )

    new_version_tag_name = f'{args.prefix}{new_version}'

    if args.create_tag and has_changes:
        create_tag(new_version_tag_name)

    # clear the output to ensure that it is empty
    clear_github_output()

    set_github_output('version', new_version)
    set_github_output('version-name', new_version_tag_name)
    set_github_output('has-changes', str(has_changes).lower())

    print_github_actions_output()

    logger.info('Version is %s', new_version)


if __name__ == '__main__':
    main()
