import json
import subprocess
import sys
from argparse import ArgumentParser

import semver


def increment_hotfix(version: str, hotfix_suffix: str) -> str:
    """
    Increment the hotfix version (-h.) or append -h.1, if the suffix does not exist.

    :param version: The old version
    :param hotfix_suffix: The suffix that should be used for the hotfix number
    :return: The new version
    """
    return semver.bump_prerelease(version, hotfix_suffix)


def get_next_version() -> tuple[str, bool]:
    """
    Determine the next version and if there are any changes from the last version.

    :return: A tuple of the next version and whether there are any new changes
    """
    process = subprocess.run(
        ('get-next-version', '--target', 'json'),
        capture_output=True,
        check=True,
        text=True
    )

    result = json.loads(process.stdout)
    return result['version'], result['hasNextVersion']


def main() -> None:
    """Increment the hotfix version if needed."""
    parser = ArgumentParser(
        description='Increment the hotfix version if needed',
        allow_abbrev=False
    )

    parser.add_argument(
        '--hotfix-suffix',
        dest='hotfix_suffix',
        default='h',
        type=str,
        help='The suffix that should be used for the hotfix number'
    )

    args = parser.parse_args()

    version, has_changes = get_next_version()

    if not has_changes:
        print(version)
        sys.exit(0)

    print(increment_hotfix(version, args.hotfix_suffix))


if __name__ == '__main__':
    main()
