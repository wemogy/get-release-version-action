"""Utilities for working with the GitHub actions output."""

__all__ = ['log_github_output', 'write_github_output']

import logging
import os
from pathlib import Path

logger = logging.getLogger('wemogy.get-release-version-action')


def log_github_output() -> None:
    """Print the contents of the GITHUB_OUTPUT file."""
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    path = Path(file_path)

    with path.open('r', encoding='utf-8') as fh:
        content = fh.read()
        logger.debug('Content of GITHUB_OUTPUT file "%s":\n%s', path, content)


def write_github_output(value: str) -> None:
    """
    Write the specified string to the GitHub actions output.

    This will overwrite any other content!
    """
    file_path = os.getenv('GITHUB_OUTPUT')

    if not file_path:
        logger.warning('GITHUB_OUTPUT not in environment, skipping GitHub actions output')
        return

    path = Path(file_path)

    with path.open('w', encoding='utf-8') as fh:
        fh.write(value)
