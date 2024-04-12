"""Utilities for working with git repositories."""
import logging

import git

from .commands import run_command

logger = logging.getLogger('wemogy.get-release-version-action')

__all__ = [
    'create_git_tag',
    'get_sorted_tags'
]


def create_git_tag(version: str) -> None:
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


def get_sorted_tags(repo: git.Repo) -> list[git.TagReference]:
    """Get all tags of a repo sorted by the time of the referenced commit, newest to oldest."""
    return sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
