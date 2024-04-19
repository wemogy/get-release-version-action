"""
A GitHub Action to determine the next version by checking the commit history
for Conventional Commits with support for hotfix changes.
"""
import logging.config
from argparse import ArgumentParser

from get_release_version_action.algorithms import main
from get_release_version_action.models import Inputs
from get_release_version_action.utils import log_github_output, setup_logging, write_github_output

logger = logging.getLogger('wemogy.get-release-version-action')


def action() -> None:
    """The main entrypoint for the GitHub action."""
    parser = ArgumentParser(
        description='A GitHub Action to determine the next version by checking the commit history for Conventional '
                    'Commits with support for hotfix changes.',
        allow_abbrev=False
    )

    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        action='store_true',
        help='Print debug messages to stdout.'
    )

    parser.add_argument(
        '--prefix',
        dest='prefix',
        required=False,
        default='v',
        help='The prefix that should be prepended to the version.'
    )

    parser.add_argument(
        '--suffix',
        dest='suffix',
        required=False,
        default='NONE',
        help='The suffix that should be appended to the version (e.g. `beta`).'
    )

    parser.add_argument(
        '--reference-version-suffix',
        dest='reference_version_suffix',
        required=False,
        default='NONE',
        help='The suffix that should be replaced with the value in `suffix`.'
    )

    parser.add_argument(
        '--bumping-suffix',
        dest='bumping_suffix',
        required=False,
        default='hotfix',
        help='The suffix to append to the version (or increment if it already exists) if `only-bump-suffix` is `true`.'
    )

    parser.add_argument(
        '--only-bump-suffix',
        dest='only_bump_suffix',
        required=False,
        default='false',
        help='Bump the `bumping-suffix` instead of the version if changes were detected.'
    )

    parser.add_argument(
        '--create-tag',
        dest='create_tag',
        required=False,
        default='true',
        help='Create a git tag for the version and push it if a remote is configured.'
    )

    parser.add_argument(
        '--mode',
        dest='mode',
        required=False,
        choices=('semantic', 'hash-based'),
        default='semantic',
        help='The mode to use for determining the next version.'
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    outputs = main(Inputs.from_argparse(args))
    write_github_output(outputs.to_github_output())

    if args.verbose:
        log_github_output()


if __name__ == '__main__':
    action()
