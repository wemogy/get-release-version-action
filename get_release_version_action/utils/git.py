"""Utilities for working with git repositories."""
import logging

import git

from .commands import run_command

logger = logging.getLogger('wemogy.get-release-version-action')

__all__ = [
    'create_git_tag',
    'get_sorted_tags',
    'tag_creation_history'
]

tag_creation_history: list[str] = []


def create_git_tag(version: str, username: str, email: str) -> None:
    """Create a new git tag for the given version and push it if a remote is configured."""
    logger.info('Setting git username and email to %s <%s>', username, email)
    run_command('git', 'config', 'user.email', email)
    run_command('git', 'config', 'user.name', username)

    logger.info('Creating tag %s', version)

    # Create the tag
    run_command('git', 'tag', '--annotate', '--message', f'Release {version}', version)
    tag_creation_history.append(version)

    git_remote = run_command('git', 'remote', 'show')

    if git_remote == '':
        logger.info('No remote found, skipping pushing')
        return

    run_command('git', 'push', 'origin', version)

    logger.info('Pushed tag %s to remote', version)


def get_sorted_tags(repo: git.Repo) -> list[git.TagReference]:
    """Get all tags of a repo sorted by the time of the referenced commit, newest to oldest."""
    return sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
