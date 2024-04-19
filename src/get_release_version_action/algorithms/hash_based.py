"""Get the next version based on the hash of the latest commit."""
import logging

import git

from get_release_version_action.models import Inputs, GetNextVersionOutput
from get_release_version_action.utils import get_sorted_tags

logger = logging.getLogger('wemogy.get-release-version-action.hash-based')

__all__ = [
    'get_next_version'
]


def build_tag_name(prefix: str, commit: git.Commit, suffix: str | None) -> str:
    """
    Build a hash-based tag name by slicing the ``hexsha`` string to the first seven characters.
    Git often abbreviates hashes to seven characters as this is usually enough to uniquely identify a commit.
    """
    return prefix + commit.hexsha[:7] + (f'-{suffix}' if suffix is not None else '')


def get_current_version(repo: git.Repo, prefix: str, suffix: str | None) -> str | None:
    """
    Get the current version (= the latest git tag that matches the versioning schema).
    If there are no tags, return ``None``.
    """
    for tag in get_sorted_tags(repo):
        tag_name = build_tag_name(prefix, tag.commit, suffix)

        # Check if the tag name starts with the specified prefix
        if tag.name == tag_name:
            logger.debug('Found tag %s (%s)', tag.name, tag.commit.hexsha[:7])
            return tag.commit.hexsha[:7]

    logger.debug('Found no tags that have the prefix %s and the suffix %s', prefix, suffix)
    return None


def get_next_version(inputs: Inputs, repo: git.Repo) -> GetNextVersionOutput:
    """
    Get the next version based on the hash of the latest commit.

    :returns: A tuple of the current version name, the next version and if the version was bumped.
    """
    current_version = get_current_version(
        repo,
        inputs.prefix,
        inputs.reference_version_suffix
    )

    next_version = repo.head.commit.hexsha[:7]
    version_bumped = current_version != next_version

    if not version_bumped:
        logger.info('No changes detected, version stays the same.')
    else:
        logger.info('Hash based version will be bumped.')

    return (
        current_version,
        next_version,
        version_bumped
    )
