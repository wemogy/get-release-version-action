import json
import subprocess
from argparse import ArgumentParser
import os
import logging
import logging.config
from pathlib import Path

import yaml
import semver

logger = logging.getLogger('wemogy.get-release-version-action')


def setup_logging():
    current_file_path = Path(__file__).resolve()
    config_file = current_file_path.parent / 'logging.config.yaml'
    with config_file.open('r') as config_stream:
        config = yaml.load(config_stream, yaml.SafeLoader)

    logging.config.dictConfig(config)
    logging.getLogger().setLevel(logging.DEBUG)


def increment_hotfix(version: str, hotfix_suffix: str) -> str:
    """
    Increment the hotfix version (-h.) or append -h.1, if the suffix does not exist.

    :param version: The old version
    :param hotfix_suffix: The suffix that should be used for the hotfix number
    :return: The new version
    """
    return semver.bump_prerelease(version, hotfix_suffix)


def get_next_version(get_next_version_path: str) -> tuple[str, bool]:
    """
    Determine the next version and if there are any changes from the last version.

    :param get_next_version_path: The path to the get-next-version executable
    :return: A tuple of the next version and whether there are any new changes
    """
    process = subprocess.run(
        (get_next_version_path, '--target', 'json'),
        capture_output=True,
        check=True,
        text=True
    )

    result = json.loads(process.stdout)
    return result['version'], result['hasNextVersion']


def create_tag(version: str) -> None:
    """
    Create a new git tag for the given version and push it if a remote is configured.

    :param version: The version that the tag should be named
    """
    # Create the tag
    subprocess.run(
        ('git', 'tag', version),
        check=True
    )

    show_remote_process = subprocess.run(
        ('git', 'remote', 'show'),
        capture_output=True,
        check=True,
        text=True
    )

    if show_remote_process.stdout == '':
        logger.info('No remote found, skipping pushing')
        return

    subprocess.run(
        ('git', 'push'),
        check=True
    )


def main() -> None:
    """Increment the hotfix version if needed."""
    setup_logging()

    parser = ArgumentParser(
        description='Increment the hotfix version if needed.',
        allow_abbrev=False
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
        type=bool,
        default=False,
        help='Only increases the suffix increment if any change got detected.'
    )

    parser.add_argument(
        '--create-tag',
        dest='create_tag',
        type=bool,
        default=False,
        help='Create a Git Tag for the version and push it if a remote is configured.'
    )

    parser.add_argument(
        '--get-next-version-path',
        dest='get_next_version_path',
        type=str,
        default='./get-next-version',
        help='Only increases the suffix increment if any change got detected'
    )

    args = parser.parse_args()

    next_version, has_changes = get_next_version(args.get_next_version_path)

    if has_changes:
        logger.info('Changes detected.')

        if args.only_increase_suffix:  # Example case: Hotfix
            logger.info('Only the suffix will be incremented.')
            new_version = increment_hotfix(next_version, args.suffix)
        else:  # Example case: New Release
            logger.info('Semantic Version will be incremented.')
            new_version = next_version
    else:  # Example case: No change, that requires a semantic version increase
        logger.info('No changes detected.')
        logger.info('Version stays the same.')
        new_version = next_version

    if args.create_tag:
        create_tag(new_version)

    os.environ['GITHUB_OUTPUT'] = f'version={new_version}'
    os.environ['GITHUB_OUTPUT'] += f'has-changes={has_changes}'
    logger.info('New version is %s', new_version)


if __name__ == '__main__':
    main()
