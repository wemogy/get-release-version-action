"""Utilities for working with the GitHub actions output."""
import logging
import os

logger = logging.getLogger('wemogy.get-release-version-action')

__all__ = [
    'log_github_output',
    'write_github_output'
]


def log_github_output() -> None:
    """Print the contents of the GITHUB_OUTPUT file."""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    # noinspection PyBroadException
    try:
        with open(file_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
            logger.debug('Content of GITHUB_OUTPUT file "%s":\n%s', file_path, content)
    except Exception:  # pylint: disable=broad-exception-caught
        # Catching every exception since this function is not necessary for the script to run
        logger.warning('An exception was ignored while trying to get contents of GITHUB_OUTPUT file', exc_info=True)


def write_github_output(value: str) -> None:
    """
    Write the specified string to the GitHub actions output.
    This will overwrite any other content!
    """
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    with open(file_path, 'w', encoding='utf-8') as fh:
        fh.write(value)
